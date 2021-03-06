import os, sys, time, shutil
import fileops, cropframes
import keyframes


def main():

	if sys.argv[1] == 'labels':

		main_dir = './full-clips/train/'
		annotations_file = '_new_shot_type_testuser.txt'

		dir_list = sorted(os.listdir(main_dir))

		label_data = []
		for dir_name in dir_list:
			if os.path.isdir(main_dir + dir_name):
			
				if os.path.exists(main_dir + dir_name + '/' + dir_name + annotations_file):
					with open(main_dir + dir_name + '/' + dir_name + annotations_file) as labels_file:
						labels = labels_file.readlines()
					labels = [label.split('\t')[0] for label in labels]
					label_data += labels
					print dir_name, len(labels)

		label_data = [label + '\n' for label in label_data]
		print len(label_data)

		with open('./train_labels_list.txt', 'w') as file:
			file.writelines(label_data)			

	elif sys.argv[1] == 'commercials':				## py org.py commercials /home/sxg755/dataset/train/all_frames/new_labels_list.txt /home/sxg755/dataset/train/all_frames/new_sorted_keyframes_list.txt
													## ~/dataset/train/8class_train_keyframes/

		labels_f = sys.argv[2]						
		keyframes_f = sys.argv[3]
		main_dir = sys.argv[4]						## /home/sxg755/dataset/train/new_5class_train_keyframes/


		# train_label_dir = '/home/sxg755/dataset/train/all_frames/labels_list.txt'
		# test_label_dir = '/home/sxg755/dataset/test/all_frames/labels_list.txt'
		
		# train_frames = '/home/sxg755/dataset/train/all_frames/cropped/'
		# test_frames = '/home/sxg755/dataset/test/all_frames/cropped/'

		# train_dir = '/home/sxg755/dataset/train/'
		# test_dir = '/home/sxg755/dataset/test/'
		
		label_dir = labels_f.rsplit('/',1)[0] + '/'
		frames_path = label_dir + 'cropped/'
		trainset_dir = label_dir.rsplit('/',2)[0] + '/'
		
		if not os.path.exists(main_dir):
			os.makedirs(main_dir)
		
		with open(labels_f, 'r') as lf:
			label_data = lf.readlines()
		label_data = [label.split('\n')[0] for label in label_data]
		with open(keyframes_f, 'r') as kf:
			all_frames = kf.readlines()
		all_frames = [keyframe.split('\n')[0] for keyframe in all_frames]
		keyframes_path = [frames_path + keyframe for keyframe in all_frames]

		with open(main_dir + 'data.txt', 'w') as file: pass

		final_list = []
		for idx, label in enumerate(label_data):
			if label not in ['Commercial','Problem/Unclassified', 'Black']:
				
				if label == 'Background_roll' or label == 'Background roll':	
					label = 'Background_roll'
					final_list.append(main_dir + all_frames[idx] + ' 0\n')
					with open(main_dir + 'data.txt', 'aw') as file:
						file.write(main_dir + all_frames[idx] + ' 0\n')
				
				elif label == 'Graphic':
					final_list.append(main_dir + all_frames[idx] + ' 1\n')
					with open(main_dir + 'data.txt', 'aw') as file:
						file.write(main_dir + all_frames[idx] + ' 1\n')				
				
				elif label == 'Weather' or label == 'Weather/Graphic' or label == 'Weather/Person':
					print 'Weather ', all_frames[idx]
					label = 'Weather'				
					final_list.append(main_dir + all_frames[idx] + ' 2\n')
					with open(main_dir + 'data.txt', 'aw') as file:
						file.write(main_dir + all_frames[idx] + ' 2\n')
				
				elif label == 'Sports':
					final_list.append(main_dir + all_frames[idx] + ' 3\n')
					with open(main_dir + 'data.txt', 'aw') as file:
						file.write(main_dir + all_frames[idx] + ' 3\n')
				
				elif label == 'Studio':
					print 'Studio ', all_frames[idx]		
					label = 'Newsperson(s)'
					final_list.append(main_dir + all_frames[idx] + ' 4\n')
					with open(main_dir + 'data.txt', 'aw') as file:
						file.write(main_dir + all_frames[idx] + ' 4\n')
				
				elif label == 'Reporter':
					label = 'Newsperson(s)'				
					final_list.append(main_dir + all_frames[idx] + ' 4\n')
					with open(main_dir + 'data.txt', 'aw') as file:
						file.write(main_dir + all_frames[idx] + ' 4\n')
				
				elif label == 'Hybrid' or label == 'Talking_head/Hybrid':
					label = 'Newsperson(s)'
					final_list.append(main_dir + all_frames[idx] + ' 4\n')
					with open(main_dir + 'data.txt', 'aw') as file:
						file.write(main_dir + all_frames[idx] + ' 4\n')
				
				elif label == 'Talking_head':
					final_list.append(main_dir + all_frames[idx] + ' 0\n')
					with open(main_dir + 'data.txt', 'aw') as file:
						file.write(main_dir + all_frames[idx] + ' 0\n')

				shutil.copy(frames_path + all_frames[idx], main_dir)

		# with open(main_dir + 'data.txt', 'aw') as file:
		# 	file.writelines(final_list)
		print len(final_list)
		
	elif sys.argv[1] == 'count':

		# with open('/home/sxg755/dataset/train/all_frames/new_sorted_keyframes_list.txt', 'r') as f:
		with open('/home/sxg755/dataset/train/new_5class_train_keyframes/data.txt', 'r') as f:
			files = f.readlines()

		with open('/home/sxg755/dataset/train/new_5class_train_keyframes/data_new.txt','w') as new_f: pass

		# cur = ''
		# count = 0
		for file in files:
			path = file.split(' ')[0]
			name = path.rsplit('_',1)[0]
			name = name.rsplit('/',1)[1]
			if name not in ['2015-06-06_1400_US_MSNBC_Melissa_Harris-Perry','2015-09-09_1600_US_KNBC_Today_Show','2014-07-12_1200_US_CNN_New_Day_Saturday','2014-02-14_2330_US_CNN_Crossfire','2014-08-18_2300_US_FOX-News_On_the_Record_with_Greta_Van_Susteren','2015-01-01_2330_US_KCAL_Inside_Edition','2015-07-07_2300_US_KCAL_KCAL_9_News_at_4PM','2015-10-22_1700_US_HLN_The_Daily_Share','2014-08-18_2000_US_HLN_HLN_News_Now','2014-01-01_2200_US_HLN_HLN_Evening_Express','2015-09-14_2100_US_WEWS_Live_on_5','2014-05-19_2258_US_WKYC_Channel_3_News_at_7','2014-03-25_1753_US_BBC_BBC_Persian','2014-04-17_2330_DE_KCET_Deutsche_Welle_Journal','2016-09-24_1230_US_KCET_Asia_Insight','2014-05-03_1600_UK_KCET_BBC_Newsnight','2015-04-04_0330_QA_AlJazeera_Inside_Story','2014-08-18_2330_US_AlJazeera_Real_Money_with_Ali_Velshi','2015-09-09_2230_QA_AlJazeera_Fault_Lines','2014-10-28_1800_CH_TV5_Le_Journal_de_la_RTS','2015-04-15_2055_FR_France-3_Grand_Soir_3','2014-10-10_2200_FR_TV5_Le_Journal_de_France_2',
                        '2015-02-28_1800_FR_TV5_64_Minutes_Le_Monde_en_Francais','2014-11-25_1630_FR_KCET_France_24']:
				with open('/home/sxg755/dataset/train/new_5class_train_keyframes/data_new.txt','aw') as new_f:
					new_f.write(file)
				

			# if name != cur:
			# 	print cur, count
			# 	cur = name
			# 	count = 1
			# else:
			# 	count += 1


	else:
		ntg = sys.argv[1]
		# clip_path = sys.argv[1] 								## ../../dir/video.mp4
		# rel_clip_path = clip_path.rsplit('/',1)[0] + '/'		## ../../dir/
		# clip_name = clip_path.rsplit('/',1)[1]					## video.mp4
		# clip = clip_name.rsplit('.',1)[0]						## video
		# output_filename = clip 									## video
		# clip_dir = rel_clip_path								## ../../dir/

		source = os.listdir('/home/sxg755/trainset/new/')
		temp = '/home/sxg755/dataset/train/new_all_frames/'		## ../../dir/all_frames/
		if not os.path.exists(temp):
			os.makedirs(temp)

		for file in source:
			if file.endswith('.mp4'):
				clip_path = '/home/sxg755/trainset/new/' + file
				keyframe_times = keyframes.keyframes(temp, clip_path)
				keyframes_list = fileops.get_keyframeslist(temp, clip_path)

				image_files = cropframes.cropframes(temp, keyframes_list, clip_path)
				image_files = [image_file.rsplit('/',1)[1] + '\n' for image_file in image_files]

				with open('/home/sxg755/dataset/train/all_frames/keyframes_list.txt', 'aw') as file:
					file.writelines(image_files)


if __name__ == '__main__':
	main()