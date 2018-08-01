# Wrapper for `argparse`

Some sample code (with some pseudo DL framework): 

```python
from cvargparse import GPUParser, ArgFactory, Arg

from dlframework import Model, LRSchedule, Updater, Iterator, to_gpu

def main(args):
    data = load_data(args.data, args.labels)
    model = Model(args.model_weights)
    # we can select multiple GPUs. use the first GPU for the initial model creation
    
    GPU = args.gpu[0]
    if GPU >= 0:
        to_gpu(model, GPU)
    
    lr_schedule = LRSchedule(args.lr, args.lr_shift, args.lr_decrease_rate, args.lr_target)
    
    updater = Updater(model, lr_schedule, decay=args.decay)
    
    it = Iterator(data, args.batch_size)
    
    for epoch in range(args.epochs):
        for batch in it:
            updater.train(model, batch)
    
parser = GPUParser(ArgFactory([
		Arg("data", type=str),
		Arg("labels", type=str),
		Arg("model_weights", type=str),

	])\
	.epochs()\
	.batch_size()\
	.learning_rate(lr=1e-3)\
	.weight_decay(5e-3)\
	.seed()\
	.debug())

parser.init_logger()
main(parser.parse_args())

```

