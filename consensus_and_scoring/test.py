from Weighting import launch_Weighting
from pointAssignment import pointSort
from Separator import indicesToStartEnd
# scoring_dir = '../data/out_scoring/'
# tua_dir ='../data/tags/'
# reporting = True
# input_dir = '../data/datahunts/'
#
# weights = launch_Weighting(scoring_dir)
# print("SORTING POINTS")
# tuas, weights, tua_raw = pointSort(scoring_dir, input_dir=input_dir, weights=weights, tua_dir=tua_dir, reporting=reporting)
arr = [1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105]
o = indicesToStartEnd(arr)
print(o)

arr = []
o = indicesToStartEnd(arr)
print(o)