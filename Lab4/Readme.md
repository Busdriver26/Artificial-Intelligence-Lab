**基于匿名差旅费用报告数据集，对异常记录进行检测**

数据量：10000

正样本：7500

负样本：2500

属性：

GAP_between_Create_Last创建日期和最后提交日期之间的间隔天数；TOTAL_EXPENSED_AMOUNT费用总额；

APPROVED_AMT批准金额；

PAID_IN_AMOUNT_ALLOCATION已付金额分配；

EXPENSE_TYPE_DESC费用类型；

CITY城市；

 

Label表示差旅费报表数据行为是否异常，0为正常，1为异常

 

 

 

•   **实践：**

Ø 利用sklearn编程环境接口

Ø 使用和对比几种不同分类算法的效果

Ø 验证train、test、validation构建策略对最终效果的影响

Ø 对比决策树剪枝、线性分类器特征重要性的影响