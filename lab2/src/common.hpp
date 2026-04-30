#include <libsnark/common/default_types/r1cs_gg_ppzksnark_pp.hpp>
#include <libsnark/zk_proof_systems/ppzksnark/r1cs_gg_ppzksnark/r1cs_gg_ppzksnark.hpp>
#include <libsnark/gadgetlib1/pb_variable.hpp>

using namespace libsnark;
using namespace std;

// 定义使用的有限域
typedef libff::Fr<default_r1cs_gg_ppzksnark_pp> FieldT;

// 定义创建面包板的函数
protoboard<FieldT> build_protoboard(int* secret)
{
    // 初始化曲线参数
    default_r1cs_gg_ppzksnark_pp::init_public_params();
    // 创建面包板
    protoboard<FieldT> pb;

    // 定义所有需要外部输入的变量以及中间变量
    pb_variable<FieldT> out;   // 公开输出
    pb_variable<FieldT> x;     // 私密输入 x
    pb_variable<FieldT> sym_1; // 中间变量 x^2
    pb_variable<FieldT> y;     // 中间变量 x^3

    // 将各个变量与 protoboard 连接
    out.allocate(pb, "out");
    x.allocate(pb, "x");
    sym_1.allocate(pb, "sym_1");
    y.allocate(pb, "y");

    // 声明与 pb 连接的前 1 个变量是 public 的 (即 out)
    pb.set_input_sizes(1);

    // 添加 R1CS 约束
    // 1. x * x = sym_1
    pb.add_r1cs_constraint(r1cs_constraint<FieldT>(x, x, sym_1));
    // 2. sym_1 * x = y
    pb.add_r1cs_constraint(r1cs_constraint<FieldT>(sym_1, x, y));
    // 3. (y + x + 5) * 1 = out
    pb.add_r1cs_constraint(r1cs_constraint<FieldT>(y + x + 5, 1, out));

    // 为变量赋值：无论是生成证明还是验证，公开结果 out 都是 35
    pb.val(out) = 35;

    // 证明者在生成证明阶段传入私密输入
    if (secret != NULL)
    {
        pb.val(x) = secret[0];
        pb.val(sym_1) = secret[1];
        pb.val(y) = secret[2];
    }

    return pb;
}
