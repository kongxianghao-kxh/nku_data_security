#include <libsnark/common/default_types/r1cs_gg_ppzksnark_pp.hpp>
#include <libsnark/zk_proof_systems/ppzksnark/r1cs_gg_ppzksnark/r1cs_gg_ppzksnark.hpp>
#include <fstream>
#include "common.hpp"

using namespace libsnark;
using namespace std;

int main()
{
    // 输入秘密值 x (在这个实验中正确解应该是 3)
    int x;
    cout << "请输入秘密解 x: ";
    cin >> x;

    // 为私密输入提供具体数值
    int secret[3];
    secret[0] = x;           // x
    secret[1] = x * x;       // x^2
    secret[2] = x * x * x;   // x^3

    // 构造面包板
    protoboard<FieldT> pb = build_protoboard(secret);
    
    // 加载证明密钥
    fstream f_pk("pk.raw", ios_base::in);
    r1cs_gg_ppzksnark_proving_key<libff::default_ec_pp> pk;
    f_pk >> pk;
    f_pk.close();

    // 生成证明
    const r1cs_gg_ppzksnark_proof<default_r1cs_gg_ppzksnark_pp> proof = r1cs_gg_ppzksnark_prover<default_r1cs_gg_ppzksnark_pp>(pk, pb.primary_input(), pb.auxiliary_input());

    // 将生成的证明保存到 proof.raw 文件
    fstream pr("proof.raw", ios_base::out);
    pr << proof;
    pr.close();

    cout << "已生成证明至 proof.raw" << endl;
    return 0;
}
