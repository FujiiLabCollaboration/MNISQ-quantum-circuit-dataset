#include <vector>
#include <deque>
#include <math.h>
#include <complex>
#include <omp.h>
#include <random>
#include <Eigen/Core>
#include <Eigen/Dense>
#include <cppsim/state.hpp>
#include <cppsim/gate_factory.hpp>
#include <cppsim/gate_matrix.hpp>

typedef Eigen::Matrix<std::complex<double>, 4, 4> Matrix4C; // 4×4複素行列
typedef Eigen::Matrix<std::complex<double>, 2, 2> Matrix2C;

#define J (1.0id)

Matrix4C kron(Matrix2C A, Matrix2C B)
{
  Matrix4C ret;
  for (int i = 0; i < 2; i++)
  {
    for (int j = 0; j < 2; j++)
    {
      for (int k = 0; k < 2; k++)
      {
        for (int l = 0; l < 2; l++)
        {
          ret(2 * i + k, 2 * j + l) = A(i, j) * B(k, l);
        }
      }
    }
  }
  return ret;
}

Eigen::Matrix4d real(Matrix4C A)
{
  Eigen::Matrix4d ret;
  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 4; j++)
      ret(i, j) = A(i, j).real();
  }
  return ret;
}

Eigen::Matrix4d imag(Matrix4C A)
{
  Eigen::Matrix4d ret;
  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 4; j++)
      ret(i, j) = A(i, j).imag();
  }
  return ret;
}

static Matrix2C I_matrix = (Matrix2C() << 1.0, 0.0, 0.0, 1.0).finished();
static Matrix2C X_matrix = (Matrix2C() << 0.0, 1.0, 1.0, 0.0).finished();
static Matrix2C Y_matrix = (Matrix2C() << 0.0, -J, J, 0.0).finished();
static Matrix2C Z_matrix = (Matrix2C() << 1.0, 0.0, 0.0, -1.0).finished();
static Eigen::Matrix4d two_qubits_Pauli[4][4] = {{real(kron(I_matrix, I_matrix)), real(kron(X_matrix, I_matrix)), imag(kron(Y_matrix, I_matrix)), real(kron(Z_matrix, I_matrix))},
                                                 {real(kron(I_matrix, X_matrix)), real(kron(X_matrix, X_matrix)), imag(kron(Y_matrix, X_matrix)), real(kron(Z_matrix, X_matrix))},
                                                 {imag(kron(I_matrix, Y_matrix)), imag(kron(X_matrix, Y_matrix)), real(kron(Y_matrix, Y_matrix)), imag(kron(Z_matrix, Y_matrix))},
                                                 {real(kron(I_matrix, Z_matrix)), real(kron(X_matrix, Z_matrix)), imag(kron(Y_matrix, Z_matrix)), real(kron(Z_matrix, Z_matrix))}};
static std::vector<std::vector<QuantumGateBase *>> Pauli_Gate;

QuantumState get_state(int n_qubits, std::deque<QuantumGateMatrix *> C, int initial_state)
{
  QuantumState state(n_qubits);
  state.set_computational_basis(initial_state);
  for (int k = 0; k < C.size(); k++)
    C[k]->update_quantum_state(&state);
  return state;
}

double get_cost(QuantumState &target_state, std::deque<QuantumGateMatrix *> C, int initial_state)
{
  int n_qubits = target_state.qubit_count;
  QuantumState state = get_state(n_qubits, C, initial_state);
  std::complex<double> f = state::inner_product(&state, &target_state);
  return 1 - std::pow(std::abs(f), 1 / (double)n_qubits);
}

Eigen::Matrix4d evaluate_F(QuantumState &target_state, QuantumState &Phi_state, QuantumState &Psi_state, unsigned int i, unsigned int j)
{
  int n_qubits = target_state.qubit_count;

  QuantumState Pauli_Psi_state = QuantumState(n_qubits);

  Eigen::Matrix4d F = Eigen::Matrix4d::Zero();
  for (int k = 0; k < 4; k++)
  {
    for (int l = 0; l < 4; l++)
    {
      Pauli_Psi_state.load(&Psi_state);
      Pauli_Gate[i][k]->update_quantum_state(&Pauli_Psi_state);
      Pauli_Gate[j][l]->update_quantum_state(&Pauli_Psi_state);
      std::complex<double> f_kl = state::inner_product(&Phi_state, &Pauli_Psi_state) / 4.0;

      if ((k == 2 || l == 2) && k != l)
      {
        F -= f_kl.imag() * two_qubits_Pauli[k][l];
      }
      else
      {
        F += f_kl.real() * two_qubits_Pauli[k][l];
      }
    }
  }

  return F;
}

Eigen::Matrix4d evaluate_Rho(QuantumState &target_state, QuantumState &Psi_state, unsigned int i, unsigned int j)
{
  int n_qubits = target_state.qubit_count;

  QuantumState Pauli_Psi_state = QuantumState(n_qubits);

  Eigen::Matrix4d Rho = Eigen::Matrix4d::Zero();
  for (int k = 0; k < 4; k++)
  {
    for (int l = 0; l < 4; l++)
    {
      Pauli_Psi_state.load(&Psi_state);
      Pauli_Gate[i][k]->update_quantum_state(&Pauli_Psi_state);
      Pauli_Gate[j][l]->update_quantum_state(&Pauli_Psi_state);
      std::complex<double> rho_kl = state::inner_product(&Psi_state, &Pauli_Psi_state) / 4.0;
      if ((k == 2 || l == 2) && k != l)
        Rho -= rho_kl.imag() * two_qubits_Pauli[k][l];
      else
        Rho += rho_kl.real() * two_qubits_Pauli[k][l];
    }
  }

  return Rho;
}

std::pair<std::deque<QuantumGateMatrix *>, int> AQCE(QuantumState &target_state, int M_0, int M_delta, int N, int M_max)
{
  int n_qubits = target_state.qubit_count;

  std::cout << "Finding maximum fidelity" << std::endl;
  double maximum_fidelity = 0;
  int initial_state = 0;
  QuantumState state = QuantumState(n_qubits);
  for (int i = 0; i < (1 << n_qubits); ++i)
  {
    state.set_computational_basis(i);
    CPPCTYPE fidelity = state::inner_product(&state, &target_state);
    if (fidelity.real() > maximum_fidelity)
    {
      std::cout << "Fidelity update " << maximum_fidelity << " -> " << fidelity.real() << std::endl;
      maximum_fidelity = fidelity.real();
      initial_state = i;
    }
  }
  std::cout << "Initial state: " << initial_state << std::endl;

  auto I_gate = gate::DenseMatrix(0, I_matrix);
  std::deque<QuantumGateMatrix *> C(M_0, I_gate);
  std::deque<QuantumGateMatrix *> C_inv(M_0, I_gate);
  int M = M_0;
  QuantumState Psi_state(n_qubits);
  QuantumState Phi_state(n_qubits);
  Pauli_Gate.assign(n_qubits, std::vector<QuantumGateBase *>(4));
  for (int i = 0; i < n_qubits; i++)
  {
    Pauli_Gate[i][0] = gate::Identity(i);
    Pauli_Gate[i][1] = gate::X(i);
    Pauli_Gate[i][2] = gate::Y(i);
    Pauli_Gate[i][3] = gate::Z(i);
  }

  std::pair<int, int> prev_select_qubit;
  while (M < M_max)
  {
    for (int add_count = 0; add_count < M_delta; add_count++)
    {
      double max = -1;
      unsigned int max_i, max_j;
      Eigen::Matrix4d V;

      Psi_state.load(&target_state);
      for (int k = M - 1; k >= 0; k--)
        C_inv[k]->update_quantum_state(&Psi_state);

      std::vector<std::vector<Eigen::SelfAdjointEigenSolver<Eigen::Matrix4d>>> eigen_list; // 各indexでの固有値,固有ベクトル結果の格納用vector
      eigen_list.resize(n_qubits);                                                         // サイズは n_qubits × n_qubits
      for (int i = 0; i < n_qubits; i++)
        eigen_list[i].resize(n_qubits);
#pragma omp parallel for
      for (int i = 0; i < n_qubits; i++)
      {
        for (int j = i + 1; j < n_qubits; j++)
        {
          Eigen::Matrix4d Rho = evaluate_Rho(target_state, Psi_state, i, j);
          Eigen::SelfAdjointEigenSolver<Eigen::Matrix4d> eigensolver(Rho);
          eigen_list[i][j] = eigensolver;
        }
      }

      Eigen::Matrix4d T; // 列を逆順にする行列
      T << 0, 0, 0, 1,
          0, 0, 1, 0,
          0, 1, 0, 0,
          1, 0, 0, 0;
      for (int i = 0; i < n_qubits; i++)
      {
        for (int j = i + 1; j < n_qubits; j++)
        {
          if (prev_select_qubit == std::pair<int, int>{i, j})
            continue;
          if (eigen_list[i][j].eigenvalues()(3) > max)
          {
            max = eigen_list[i][j].eigenvalues()(3);
            max_i = i;
            max_j = j;
            V = eigen_list[i][j].eigenvectors() * T;
          }
        }
      }
      prev_select_qubit = std::pair<int, int>{max_i, max_j};
      std::cout << V << std::endl;
      Eigen::Matrix<double, 4, 1> now = eigen_list[max_i][max_j].eigenvalues();
      V = eigen_list[max_i][max_j].eigenvectors() * T;
      auto V_gate = gate::DenseMatrix({max_i, max_j}, V);
      auto V_inv_gate = gate::DenseMatrix({max_i, max_j}, V.transpose());
      C.push_front(V_gate);
      C_inv.push_front(V_inv_gate);
      M++;
    }

    for (int sweep_count = 0; sweep_count < N; sweep_count++)
    {
      for (int m = 0; m < M; m++)
      {
        double max = -1;
        unsigned int max_i, max_j;
        Eigen::Matrix4d U;

        Phi_state.set_computational_basis(initial_state);
        for (int k = 0; k < m; k++)
          C[k]->update_quantum_state(&Phi_state);

        Psi_state.load(&target_state);
        for (int k = M - 1; k >= m + 1; k--)
          C_inv[k]->update_quantum_state(&Psi_state);

        std::vector<std::vector<Eigen::JacobiSVD<Eigen::Matrix4d>>> svd_list; // 各indexでのSVD結果の格納用vector
        svd_list.resize(n_qubits);                                            // サイズは n_qubits × n_qubits
        for (int i = 0; i < n_qubits; i++)
          svd_list[i].resize(n_qubits);
#pragma omp parallel for
        for (int i = 0; i < n_qubits; i++)
        {
          for (int j = i + 1; j < n_qubits; j++)
          {
            Eigen::Matrix4d F = evaluate_F(target_state, Phi_state, Psi_state, i, j);
            Eigen::JacobiSVD<Eigen::Matrix4d> svd(F, Eigen::ComputeFullU | Eigen::ComputeFullV);
            svd_list[i][j] = svd;
          }
        }

        for (int i = 0; i < n_qubits; i++)
        {
          for (int j = i + 1; j < n_qubits; j++)
          {
            if (svd_list[i][j].singularValues().sum() > max)
            {
              max = svd_list[i][j].singularValues().sum();
              max_i = i;
              max_j = j;
              U = svd_list[i][j].matrixU() * svd_list[i][j].matrixV().transpose();
            }
          }
        }

        auto U_gate = gate::DenseMatrix({max_i, max_j}, U);
        auto U_inv_gate = gate::DenseMatrix({max_i, max_j}, U.transpose());
        C[m] = U_gate;
        C_inv[m] = U_inv_gate;
      }
    }
    std::cout << "cost  " << get_cost(target_state, C, initial_state) << std::endl;
    std::cout << "M  " << M << std::endl;
  }
  return {C, initial_state};
}

std::vector<std::string> split(const std::string &s, char delim)
{
  std::vector<std::string> elems;
  std::string item;
  for (char ch : s)
  {
    if (ch == delim)
    {
      if (!item.empty())
        elems.push_back(item);
      item.clear();
    }
    else
    {
      item += ch;
    }
  }
  if (!item.empty())
    elems.push_back(item);
  return elems;
}

void output(std::deque<QuantumGateMatrix *> C, int initial_state, std::ofstream &out)
{
  out << "OPENQASM 2.0;" << std::endl;
  out << "include \"qelib1.inc\";" << std::endl;
  out << "qreg q[10];" << std::endl;
  for (int i = 0; i < 10; ++i)
  {
    if ((1 << i) & initial_state)
      out << "x q[" << i << "];" << std::endl;
  }
  for (auto x : C)
  {
    assert(x->get_target_index_list().size() == 2);
    out << "DenseMatrix(2,0";
    std::vector<std::string> now = split(x->to_string(), '\n');
    std::vector<double> matrix;
    for (int i = 12; i < 16; i++)
    {
      double a, b, c, d, e, f, g, h;
      sscanf(now[i].c_str(), " (%lf,%lf) (%lf,%lf) (%lf,%lf) (%lf,%lf)", &a, &b, &c, &d, &e, &f, &g, &h);
      matrix.push_back(a);
      matrix.push_back(b);
      matrix.push_back(c);
      matrix.push_back(d);
      matrix.push_back(e);
      matrix.push_back(f);
      matrix.push_back(g);
      matrix.push_back(h);
    }
    for (int i = 0; i < matrix.size(); ++i)
    {
      out << "," << matrix[i];
    }
    out << ") q[" << x->get_target_index_list()[0] << "],q[" << x->get_target_index_list()[1] << "];" << std::endl;
  }
}

int main(int argc, char *argv[])
{
  int n_qubits = 10;
  int dim = 1 << n_qubits;
  CPPCTYPE coef[dim];

  std::string infile = argv[1];
  std::string circuit_outfile = argv[2];
  std::string fidelity_outfile = argv[3];
  std::ifstream fin(infile);
  std::ofstream circuit_out(circuit_outfile);
  std::ofstream fidelity_out(fidelity_outfile);

  std::string M_0_str = argv[4];
  std::string M_delta_str = argv[5];
  std::string N_str = argv[6];
  std::string M_max_str = argv[7];
  int M_0 = stoll(M_0_str);
  int M_delta = stoll(M_delta_str);
  int N = stoll(N_str);
  int M_max = stoll(M_max_str);

  srand((unsigned)time(NULL));
  for (int i = 0; i < dim; i++)
  {
    double a, b;
    fin >> a >> b;
    coef[i] = {a, b};
  }

  QuantumState target_state(n_qubits);
  target_state.load(coef);
  double norm_factor = target_state.get_squared_norm();
  target_state.normalize(norm_factor);

  std::pair<std::deque<QuantumGateMatrix *>, int> circuit = AQCE(target_state, M_0, M_delta, N, M_max);
  output(circuit.first, circuit.second, circuit_out);
  circuit_out.close();

  QuantumState real_state = get_state(n_qubits, circuit.first, circuit.second);
  CPPCTYPE fidelity = state::inner_product(&target_state, &real_state);
  fidelity_out << fidelity.real() << std::endl;
}
