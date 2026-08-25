import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding
)
from sklearn.metrics import confusion_matrix, accuracy_score


def preprocess_Data(path):
    df = pd.read_csv(path, encoding='utf-8')
    # df = df[df['is_fraud'].isin(['TRUE', 'FALSE'])]
    for x in df.index:
        # print(df.loc[x, 'is_fraud'])
        if df.loc[x, 'is_fraud'] != True and df.loc[x, 'is_fraud'] != False:
            df.drop(x, inplace=True)
    return df


def compute_metrics(eval_pred):
    """计算评估指标：总体准确率、诈骗类准确率、非诈骗类准确率"""
    predictions, labels = eval_pred
    pred_labels = np.argmax(predictions, axis=1)  # 取概率最大的标签

    # 混淆矩阵：TN（真负）、FP（假正）、FN（假负）、TP（真正）
    tn, fp, fn, tp = confusion_matrix(labels, pred_labels).ravel()

    # 计算指标
    total_accuracy = accuracy_score(labels, pred_labels)
    fraud_accuracy = tp / (tp + fn) if (tp + fn) > 0 else 0.0  # 诈骗类准确率（召回率）
    nonfraud_accuracy = tn / (tn + fp) if (tn + fp) > 0 else 0.0  # 非诈骗类准确率

    return {
        'total_accuracy': total_accuracy,
        'fraud_accuracy': fraud_accuracy,
        'nonfraud_accuracy': nonfraud_accuracy
    }


class FraudDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        # 对对话文本进行分词编码
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        # 转换为单样本张量
        item = {key: val.flatten() for key, val in encoding.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item


def main(train_path, test_path, model_save_dir='./bert_fraud_model'):
    # 加载数据
    train_df = preprocess_Data(train_path)
    test_df = preprocess_Data(test_path)

    # 新增：检查数据量
    print(f"训练集样本数：{len(train_df)}")  # 若为0则说明问题所在
    print(f"测试集样本数：{len(test_df)}")

    # 加载中文bert分词器和模型
    model_name = 'bert-base-chinese'
    local_model_dir = 'google-bert/bert-base-chinese'
    tokenizer = BertTokenizer.from_pretrained(local_model_dir)
    # 加载bert用于对序列文本进行分类的模型
    model = BertForSequenceClassification.from_pretrained(
        local_model_dir, num_labels=2)

    print(model)
    # 冻结bert主体
    for param in model.bert.parameters():
        param.required_grad = False

    #  构建数据集
    train_dataset = FraudDataset(
        texts=train_df['specific_dialogue_content'].tolist(),
        labels=[1 if label ==
                True else 0 for label in train_df['is_fraud'].to_list()],
        tokenizer=tokenizer
    )
    test_dataset = FraudDataset(
        texts=test_df['specific_dialogue_content'].tolist(),
        labels=[1 if label ==
                True else 0 for label in test_df['is_fraud'].to_list()],
        tokenizer=tokenizer
    )

    # 训练参数配置
    training_args = TrainingArguments(
        output_dir=model_save_dir,
        num_train_epochs=1,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=100,     # 热身的steps
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=50,
        evaluation_strategy='epoch',
        save_strategy='epoch',
        load_best_model_at_end=True,
        metric_for_best_model='total_accuracy',
        fp16=torch.cuda.is_available()
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
        data_collator=DataCollatorWithPadding(
            tokenizer=tokenizer)   # 动态padding
    )

    trainer.train()
    eval_results = trainer.evaluate()
    print(f"总体准确率： {eval_results['eval_total_accuracy']:.4f}")
    print(f"诈骗类准确率： {eval_results['eval_fraud_accuracy']:.4f}")
    print(f"非诈骗类准确率： {eval_results['eval_nonfraud_accuracy']:.4f}")

    trainer.save_model(model_save_dir)
    tokenizer.save_pretrained(model_save_dir)
    print(f"模型已经保存到：{model_save_dir}")


if __name__ == '__main__':
    train_path = 'train_set.csv'
    test_path = 'test_set.csv'

    main(train_path, test_path)
