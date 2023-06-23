# dataset settings
#dataset_type = 'LoveDADataset'
dataset_type = 'LD'
#classes = ('background', 'road')
data_root = 'data/loveDA_ori' # loveDA
#data_root = 'data' # loveDA
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
    #mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225], to_rgb=True)
#crop_size = (1024, 1024)
crop_size = (512,512)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', reduce_zero_label=True),
    #dict(type='Resize', img_scale=(1024, 1024), ratio_range=(0.5, 2.0)),
    dict(type='Resize', img_scale=(512, 512), ratio_range=(0.5, 2.0)),
    dict(type='RandomCrop', crop_size=crop_size, cat_max_ratio=0.75),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PhotoMetricDistortion'),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size=crop_size, pad_val=0, seg_pad_val=255),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_semantic_seg']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(512, 512),
        #img_scale=(1024, 1024),
        # img_ratios=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75],
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
data = dict(
    samples_per_gpu=2,
    workers_per_gpu=1,
    train=dict(
        type=dataset_type,
        data_root=data_root,
        #img_dir='img_dir/train',
        #ann_dir='ann_dir/train',
        #img_dir='Train/imgs_dir', #loveDA
        #ann_dir='Train/ann_dir', 
        #img_dir='../../../../PinKunXian/zl16_images_Nov_Dec/2019/train_folder',   #work_dirs3,4
        #ann_dir='../../../../PinKunXian/osm_label_line/different_type_grid_train', 
        img_dir='../../../../PinKunXian/Unet/Pytorch-UNet-master/data/imgs',
        ann_dir='../../../../PinKunXian/Unet/Pytorch-UNet-master/data/masks_eq1', 
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        data_root=data_root,
        #img_dir='Val/imgs_dir', #loveDA
        #ann_dir='Val/ann_dir', 
        img_dir='../../../../PinKunXian/zl16_images_Nov_Dec/2019/yunyangxian',
        ann_dir='../../../../PinKunXian/osm_label_line/different_type_grid_val',
        #img_dir='img_dir/val',
        #ann_dir='ann_dir/val',
        #img_dir='../zl19_images_concat/Brimingham_short/Urban/images_png',
        #ann_dir='../zl19_images_concat/Brimingham_short/Urban/images_png',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        data_root=data_root,
        #img_dir='img_dir/val',
        #ann_dir='ann_dir/val',
        #img_dir='../zl19_images/Birmingham_short',
        #ann_dir='../zl19_images/Birmingham_short',
        #img_dir='../zl19_images_concat/Brimingham_short/Urban/images_png',
        #ann_dir='../zl19_images_concat/Brimingham_short/Urban/images_png',
        #img_dir='Val/imgs_dir',
        #ann_dir='Val/ann_dir',
        img_dir='../../../../PinKunXian/zl16_images_Nov_Dec/2019/yunyangxian',
        ann_dir='../../../../PinKunXian/osm_label_line/different_type_grid_val',
        pipeline=test_pipeline))
