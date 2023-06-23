import os
import mmcv
import mmcv_custom   # noqa: F401,F403
import mmseg_custom   # noqa: F401,F403
from mmseg.apis import inference_segmentor, init_segmentor, show_result_pyplot
from mmseg.core.evaluation import get_palette
from mmcv.runner import load_checkpoint
from mmseg.core import get_classes
import glob
import cv2
import os.path as osp
from pathlib import Path
import pandas as pd
from tqdm import tqdm
import numpy as np
import argparse
from PIL import Image
import sys
###################################################### new est

#import setproctitle
#setproctitle.setproctitle('segmentation@xyx')
#import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '3'

#INPUT_PATH = Path('../../place/image_download/zl19_images/2014/Chandler_city')
#SAVE_PATH = Path('./Segmentation_test')
#SAVE_VIS_PATH = Path('./Segmentation_Vis_test')

#####city = 'New_Orleans_city' #'Chula_Vista_city'
######year = 2014
#####INPUT_PATH = '../../image_download/zl19_images/2014/'+city

#SAVE_PATH = './Segmentation_test'
#SAVE_VIS_PATH = './Segmentation_Vis_test'

#SAVE_PATH.mkdir(exist_ok=True,parents=True)
#SAVE_VIS_PATH.mkdir(exist_ok=True,parents=True)

def main():
    args = {}
    #args['config'] = 'configs/ade20k/upernet_augreg_adapter_base_512_160k_ade20k_copy.py'
    args['config'] = 'configs/ade20k/upernet_augreg_adapter_base_512_160k_ade20k.py' #因为服务器不同
    args['checkpoint'] = 'work_dirs2/best_mIoU_iter_144000.pth'
    args['device'] = 'cuda:0'
    #args['palette'] = 'loveDADataset'
    args['opacity'] = 0.5

    classes = ('background', 'building', 'road', 'water', 'barren', 'forest',
                               'agricultural')

    LABEL_NAMES = np.asarray(['background', 'building', 'road', 'water', 'barren', 'forest',
                                       'agricultural'])

    palette = [[255, 255, 255], [255, 0, 0], [255, 255, 0], [0, 0, 255],
                                   [159, 129, 183], [0, 255, 0], [255, 195, 128]]
    
    parser = argparse.ArgumentParser(description='姓名')
    parser.add_argument('--city', type=str, help='city_name')
    parser.add_argument('--year', type=str, help='year')
    args2 = parser.parse_args()
    city = args2.city #'New_Orleans_city' #'Chula_Vista_city'
    year = args2.year #2014
    #INPUT_PATH = '../../New_folder1/zl19_images/'+str(year)+'/'+city #Feb submittion file
    INPUT_PATH = '../../sci_data_2021/zl19_images/'+str(year)+'/'+city

    city_ = city.replace(' ','_')

    print('city ',city)
    print('year ',year)
    #if os.path.exists('semseg_results/'+city_+'_'+str(year)+'_imgs_semseg.csv') or os.path.exists(' \
    #        ../../ViT-Adapter/segmentation/semseg_results/'+city_+'_'+str(year)+'_imgs_semseg.csv'):
    
    #########################Feb submittion
    #if os.path.exists('semseg_results/'+city+'_'+str(year)+'_imgs_semseg.csv'):
    #    sys.exit()

    #if os.path.exists('semseg_results_otheryear/'+city_+'_'+str(year)+'_imgs_semseg.csv'):
    #    sys.exit()

    if os.path.exists('semseg_results_212223/'+city+'_'+str(year)+'_imgs_semseg.csv'):
        sys.exit()
    #if os.path.exists('semseg_results/'+city+'_'+str(year)+'_imgs_semseg.csv') or os.path.exists(' \
    #        ../../ViT-Adapter/segmentation/semseg_results/'+city+'_'+str(year)+'_imgs_semseg.csv'):
    #    sys.exit()
    # build the model from a config file and a checkpoint file
    
    #if not os.path.exists('../../New_folder1/zl19_images/'+str(year)+'/'+city):
    if not os.path.exists('../../sci_data_2021/zl19_images/'+str(year)+'/'+city):
        city = city_

    model = init_segmentor(args['config'], checkpoint=None, device=args['device'])
    checkpoint = load_checkpoint(model, args['checkpoint'], map_location='cpu')
    if 'CLASSES' in checkpoint.get('meta', {}):
        model.CLASSES = checkpoint['meta']['CLASSES']
    else:
        model.CLASSES = classes #get_classes(args['palette'])
        #model.CLASSES = get_classes(args['palette'])

    if 'PALETTE' in checkpoint.get('meta', {}):
        model.PALETTE = checkpoint['meta']['PALETTE']
    else:
        print('"PALETTE" not found in meta, use dataset.PALETTE instead')
        model.PALETTE = dataset.PALETTE

    input_file_list = glob.glob(INPUT_PATH+'/*.png')
    print('image number: '+ str(len(input_file_list)))
    #for region in INPUT_PATH.iterdir():
    #for input_file in input_file_list[:5]:
    segmentation_df = pd.DataFrame()
    pbar = tqdm(input_file_list)
    #final_array = np.array([])
    #img_list = []
    segmentation_df = pd.DataFrame()
    
    valid_input_list = []
    invalid_input_list = []
    for input_file in pbar:
        d = Image.open(input_file)
        #d = np.array(d)
        try:
            d.load()
            #print(1)
            valid_input_list.append(input_file)
        except:
        #print(2)
            invalid_input_list.append(input_file.split('/')[-1].split('.')[0])
    #pd_dict = pd.DataFrame({'invalid_img_name': invalid_input_list})
    #pd_dict.to_csv('invalid_img_dir/'+city+'_'+str(year)+'_invalid_img.csv', index = False)
    pbar = tqdm(valid_input_list)
    for input_file in pbar:
        print(input_file) 
        #region_path = INPUT_PATH.joinpath(region.stem)
        #save_region_path = SAVE_PATH.joinpath(region.stem)
        #save_vis_region_path = SAVE_VIS_PATH.joinpath(region.stem)
        #save_region_path.mkdir(exist_ok=True,parents=True)
        #save_vis_region_path.mkdir(exist_ok=True,parents=True)
        #stitch_meta_info = pd.read_csv(region_path.joinpath('stitch_meta_info.csv'))

        #segmentation_df = pd.DataFrame()
        #for idx in tqdm(range(stitch_meta_info.shape[0])):
        #result = inference_segmentor(model, str(region_path.joinpath(stitch_meta_info.loc[idx,'file_name'])))[0]
        #img_file_name = input_file.split('/')[-1].split('.')[0]
        #img_mask = np.loadtxt('../../zl19_images_concat_msk/' + img_file_name + '.txt' )
        result = inference_segmentor(model, input_file)[0]
        tmp_seg_results = {}
        tmp_seg_results['img_name'] = input_file.split('/')[-1].split('.')[0]


            # 整理信息
        #mask_new = np.ones([1024,1024])
        #img_mask_zero_idx = np.where(img_mask==0)
        #for idx_1, idx_2 in zip(img_mask_zero_idx[0],img_mask_zero_idx[1]):
        #    mask_new[idx_1*256:(idx_1+1)*256, idx_2*256:(idx_2+1)*256] = 0

        #result_for_seg = result*mask_new
        #tmp_seg_results = {}
        #tmp_seg_results['img_name']
        for i in range(len(LABEL_NAMES)):
            tmp_seg_results[LABEL_NAMES[i]] = [np.sum(np.sum((result == i))).astype(float) / (result.shape[0] * result.shape[1])]
        segmentation_df = pd.concat([segmentation_df, pd.DataFrame(tmp_seg_results)])
    #segmentation_df.to_csv('semseg_results_otheryear/'+city+'_'+str(year)+'_imgs_semseg.csv', index=False)
    segmentation_df.to_csv('semseg_results_212223/'+city+'_'+str(year)+'_imgs_semseg.csv', index=False)
 
        #final_array = np.concatenate((final_array,result),axis = 0)
        #img_list.append(input_file.split('/')[-1].split('.')[0])
    #final_arr_pd = pd.DataFrame(final_array)
    #final_arr_pd.columns = ['background', 'building', 'road', 'water', 'barren', 'forest','agricultural']
    #img_pd = pd.DataFrame({'img_name': img_list})
    #final_dict = pd.concat([img_pd,final_arr_pd], axis = 1)
    #final_dict.to_csv('Detroit city_imgs_semseg.csv', index=False)

            # save pred results
            #cv2.imwrite(str(save_region_path.joinpath(stitch_meta_info.loc[idx,'file_name'][:-4] + '.png')), np.expand_dims(result,2).astype('uint8'))
        #cv2.imwrite((SAVE_PATH+'/'+input_file.split('/')[-1].split('.')[0]+'.png'), np.expand_dims(result,2).astype('uint8'))

            # save visable results
        #if hasattr(model, 'module'):
        #    model = model.module
        #vis = model.show_result((INPUT_PATH+'/'+input_file.split('/')[-1].split('.')[0]+'.png'), [result],
        #                        palette=palette,
        #                        #palette=get_palette(args['palette']),
        #                        show=False, opacity=args['opacity'])



        #cv2.imwrite(str(save_vis_region_path.joinpath(stitch_meta_info.loc[idx,'file_name'][:-4] + '.png')), vis)
        #cv2.imwrite(SAVE_VIS_PATH+'/'+input_file.split('/')[-1].split('.')[0]+'.png', vis)

        #segmentation_df = pd.concat([segmentation_df,pd.DataFrame(tmp_seg_results)])
    #segmentation_meta_info = stitch_meta_info.join(segmentation_df.reset_index())
    #segmentation_meta_info.to_csv(save_region_path.joinpath('segmentation_meta_info.csv'),index=False)




if __name__ == '__main__':
    main()
