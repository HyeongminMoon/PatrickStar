## PatrickStar examples

### Use PatrickStar with HuggingFace

`huggingface_bert.py` is a fine-tuning Huggingface example with Patrickstar. Could you compare it with the [official Huggingface example](https://huggingface.co/transformers/custom_datasets.html#seq-imdb) to know how to apply PatrickStar to existed projects.

Before running the example, you need to prepare the data:

```bash
wget http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
tar -xf aclImdb_v1.tar.gz
```

And change the directory used in `get_dataset()`. After these, you are ready to go:

```bash
python huggingface_bert.py
```

### Use PatrickStar to train large model

`run_bert.sh` and `pretrain_bert_demo.py` is an example to train large PTMs with PatrickStar. You could run different size of model by adding config to`run_bert.sh`.

The following command will run a model with 4B params:

```bash
env MODEL_NAME=GPT2_4B RES_CHECK=0 DIST_PLAN="patrickstar" bash run_bert.sh
```

For the available `MODEL_NAME`, please check `pretrain_bert_demo.py`.

Check the accuracy of PatrickStar with Bert:

```bash
bash RES_CHECK=1 run_bert.sh
```
