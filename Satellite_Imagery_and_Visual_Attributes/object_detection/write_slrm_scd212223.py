import glob
import pandas
import os

#num = 12
#num = 3 
#file_list = glob.glob('obd_yaml_file/*.yaml')
#file_list = glob.glob('obd_yaml_file_otheryear/*.yaml')
file_list = glob.glob('obd_yaml_file_212223/*.yaml')
#file_list = glob.glob('obd_vakka_scd_single_2018_yaml/*.yaml')
#file_list = glob.glob('obd_vakka_scd_single2_2018_yaml/*.yaml')

Npara = 6
Nlp = int(len(file_list)/Npara)

for num in range(Npara):
    if num == Npara-1:
        list_start = num*Nlp
        list_end = len(file_list)
    else:
        list_start = num*Nlp
        list_end = (num+1)*Nlp

    with open('run_od_BBJ_212223_'+str(num) +'.py',"w") as variable_name:
        variable_name.write('import os')
        variable_name.write('\n')
        variable_name.write('\n')
        for f in file_list[list_start:list_end]:
            f_name = f.split('/')[-1]
            if f_name.split('_')[1] == 'xview':
                variable_name.write('os.system('+'\''+'python val_new_212223.py --weights runs/train/expXview/weights/best.pt --data '+'\''+'+'+'\''+'\\'+'\''+ '\''+'+'+'\''+f+'\''+'+'+'\''+'\\'+'\''+ '\''+'+'+'\''+' --batch-size 50 --img 512 --save-txt --save-conf --name '+'\''+'+'+'\''+'\\'+'\''+ '\''+'+'+'\''+f_name.split('.')[0] +'\''+'+'+'\''+'\\'+'\''+ '\''+')')
                #variable_name.write('python val_new.py --weights runs/train/expXview/weights/best.pt --data '+'\''+ f +'\''+' --batch-size 50 --img 512 --save-txt --save-conf --name '+'\''+ f_name.split('.')[0]+'\'')
#            else:
            if f_name.split('_')[1] == 'DOTA':
                #variable_name.write('python val_new.py --weights runs/train/expDOTAv2/weights/best.pt --data '+'\''+ f+'\''+' --batch-size 50 --img 512 --save-txt --save-conf --name '+'\''+ f_name.split('.')[0]+'\'')
                variable_name.write('os.system('+'\''+'python val_new_212223.py --weights runs/train/expDOTAv2/weights/best.pt --data '+'\''+'+'+'\''+'\\'+'\''+ '\''+'+'+'\''+f+'\''+'+'+'\''+'\\'+'\''+ '\''+'+'+'\''+' --batch-size 50 --img 512 --save-txt --save-conf  --name '+'\''+'+'+'\''+'\\'+'\''+ '\''+'+'+'\''+f_name.split('.')[0] +'\''+'+'+'\''+'\\'+'\''+ '\''+')')
            #variable_name.write('\n')
            variable_name.write('\n')

"""
#variable_name.write('srun python val.py --weights runs/train/expXview/weights/best.pt --data '+ f  +' --batch-size 64 --img 512 --save-txt --save-conf --name ' + f_name.split('.')[0] + ' --device cpu')
            variable_name.write('\n')
#with open("run_od_gpu.slrm","w") as variable_name:
    with open('run_od_scd_'+str(num) +'.slrm',"w") as variable_name:
    #with open('run_od_scd_single_'+str(num) +'.slrm',"w") as variable_name:
    #with open('run_od_scd_single2_'+str(num) +'.slrm',"w") as variable_name:
        variable_name.write('#!/bin/bash')
        variable_name.write('\n')
        variable_name.write('\n')
    #variable_name.write('#SBATCH --job-name=od_city_gpu ')
        variable_name.write('#SBATCH --job-name=od_city_scd_'+str(num) +'')
        variable_name.write('\n')
        variable_name.write('#SBATCH -M ukko')
        variable_name.write('\n')
    #variable_name.write('#SBATCH -p short')
        variable_name.write('#SBATCH -p gpu')
        variable_name.write('\n')
        variable_name.write('#SBATCH -n 1')
        variable_name.write('\n')
        variable_name.write('#SBATCH --cpus-per-task=8')
        variable_name.write('\n')
        variable_name.write('#SBATCH --output=od_city_scd_'+str(num) +'.out')
        variable_name.write('\n')
        variable_name.write('#SBATCH --error=od_city_scd_'+str(num) +'.err')
        variable_name.write('\n')
        variable_name.write('#SBATCH --gres=gpu:1')
        variable_name.write('\n')
    #variable_name.write('#SBATCH --constraint=v100')
    #variable_name.write('\n')
        variable_name.write('#SBATCH --mem=12G')
        variable_name.write('\n')
        variable_name.write('#SBATCH --time=23:40:00')
        variable_name.write('\n') 
        variable_name.write('\n')
        variable_name.write('module load CUDA/11.1.1-GCC-10.2.0')
        variable_name.write('\n')
        variable_name.write('module load Python/3.8.6-GCCcore-10.2.0')
        variable_name.write('\n')
        variable_name.write('\n') 
        #variable_name.write('cd $PROJ/anaconda3/bin')
        variable_name.write('cd MyEnv/bin')
        variable_name.write('\n')
        variable_name.write('source activate')
        variable_name.write('\n')
        #variable_name.write('cd $WRKDIR/image_download/yolov5-master')
        variable_name.write('cd $WRKDIR/image_download/yolov5-master')
        variable_name.write('\n')
        variable_name.write('export LD_LIBRARY_PATH=/wrk-vakka/users/xiyanxin/image_download/yolov5-master/MyEnv/lib/python3.8/site-packages/torch/lib/../../nvidia/cublas/lib/:$LD_LIBRARY_PATH')
        variable_name.write('\n')

        for f in file_list[list_start:list_end]:
            f_name = f.split('/')[-1]
            if f_name.split('_')[1] == 'xview':
                variable_name.write('srun python val_new.py --weights runs/train/expXview/weights/best.pt --data '+'\'' + f +'\'' +' --batch-size 256 --img 512 --save-txt --save-conf --name ' +'\'' + f_name.split('.')[0]+'\'')
            else:
                variable_name.write('srun python val_new.py --weights runs/train/expDOTAv2/weights/best.pt --data '+'\''+ f+'\''  +' --batch-size 256 --img 512 --save-txt --save-conf --name '+'\'' + f_name.split('.')[0]+'\'')
        #variable_name.write('srun python val.py --weights runs/train/expXview/weights/best.pt --data '+ f  +' --batch-size 64 --img 512 --save-txt --save-conf --name ' + f_name.split('.')[0] + ' --device cpu')
            variable_name.write('\n')
"""
