import h5py
import numpy as np

filename = "MyWeights.h5"

# Cantidad de canales
CHANNEL = 3

# Conv1
CONV1_KERNEL_SIZE = 6   # 6x6
CONV1_FILTERS = 96
conv1_weights = np.random.normal(0, np.sqrt(2.0/CONV1_KERNEL_SIZE), (CONV1_KERNEL_SIZE, CONV1_KERNEL_SIZE, CHANNEL, CONV1_FILTERS ))
conv1_weights = np.array(conv1_weights)
conv1_bias = np.random.normal(0, np.sqrt(2.0/CONV1_FILTERS), (CONV1_FILTERS))
conv1_bias = np.array(conv1_bias)

# conv9
CONVPRED_KERNEL_SIZE = 1   # 1x1
CONVPRED_FILTERS = 54      # 9 anchors per grid and 1 class (self.config.ANCHOR_PER_GRID * (self.config.CLASSES + 1 + 4 ))
convpred_weights = np.random.normal(0, np.sqrt(2.0/CONVPRED_KERNEL_SIZE), (CONVPRED_KERNEL_SIZE, CONVPRED_KERNEL_SIZE, CHANNEL, CONVPRED_FILTERS))
convpred_weights = np.array(convpred_weights)
convpred_bias = np.random.normal(0, np.sqrt(2.0/CONVPRED_FILTERS), (CONVPRED_FILTERS))
convpred_bias = np.array(convpred_bias)

# fire define 
FIRE_KERNEL_SIZE_s1x1 = 1 # 1x1
FIRE_KERNEL_SIZE_e1x1 = 1 # 1x1
FIRE_KERNEL_SIZE_e3x3 = 3 # 3x3

# fire2 defines
FIRE2_FILTERS_s1x1 = 16
FIRE2_FILTERS_e1x1 = 64
FIRE2_FILTERS_e3x3 = 64

# fire2 weights and bias
fire2_s1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_s1x1), (FIRE_KERNEL_SIZE_s1x1, FIRE_KERNEL_SIZE_s1x1, CHANNEL, FIRE2_FILTERS_s1x1)))
fire2_s1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE2_FILTERS_s1x1), (FIRE2_FILTERS_s1x1)))
fire2_e1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e1x1), (FIRE_KERNEL_SIZE_e1x1, FIRE_KERNEL_SIZE_e1x1, CHANNEL, FIRE2_FILTERS_e1x1)))
fire2_e1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE2_FILTERS_e1x1), (FIRE2_FILTERS_e1x1)))
fire2_e3x3_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e3x3), (FIRE_KERNEL_SIZE_e3x3, FIRE_KERNEL_SIZE_e3x3, CHANNEL, FIRE2_FILTERS_e3x3)))
fire2_e3x3_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE2_FILTERS_e3x3), (FIRE2_FILTERS_e3x3)))

# fire3 defines
FIRE3_FILTERS_s1x1 = 16
FIRE3_FILTERS_e1x1 = 64
FIRE3_FILTERS_e3x3 = 64

# fire3 weights and bias
fire3_s1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_s1x1), (FIRE_KERNEL_SIZE_s1x1, FIRE_KERNEL_SIZE_s1x1, CHANNEL, FIRE3_FILTERS_s1x1)))
fire3_s1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE3_FILTERS_s1x1), (FIRE3_FILTERS_s1x1)))
fire3_e1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e1x1), (FIRE_KERNEL_SIZE_e1x1, FIRE_KERNEL_SIZE_e1x1, CHANNEL, FIRE3_FILTERS_e1x1)))
fire3_e1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE3_FILTERS_e1x1), (FIRE3_FILTERS_e1x1)))
fire3_e3x3_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e3x3), (FIRE_KERNEL_SIZE_e3x3, FIRE_KERNEL_SIZE_e3x3, CHANNEL, FIRE3_FILTERS_e3x3)))
fire3_e3x3_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE3_FILTERS_e3x3), (FIRE3_FILTERS_e3x3)))

# fire4 defines
FIRE4_FILTERS_s1x1 = 32
FIRE4_FILTERS_e1x1 = 128
FIRE4_FILTERS_e3x3 = 128

# fire4 weights and bias
fire4_s1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_s1x1), (FIRE_KERNEL_SIZE_s1x1, FIRE_KERNEL_SIZE_s1x1, CHANNEL, FIRE4_FILTERS_s1x1)))
fire4_s1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE4_FILTERS_s1x1), (FIRE4_FILTERS_s1x1)))
fire4_e1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e1x1), (FIRE_KERNEL_SIZE_e1x1, FIRE_KERNEL_SIZE_e1x1, CHANNEL, FIRE4_FILTERS_e1x1)))
fire4_e1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE4_FILTERS_e1x1), (FIRE4_FILTERS_e1x1)))
fire4_e3x3_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e3x3), (FIRE_KERNEL_SIZE_e3x3, FIRE_KERNEL_SIZE_e3x3, CHANNEL, FIRE4_FILTERS_e3x3)))
fire4_e3x3_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE4_FILTERS_e3x3), (FIRE4_FILTERS_e3x3)))

# fire5 defines
FIRE5_FILTERS_s1x1 = 32
FIRE5_FILTERS_e1x1 = 128
FIRE5_FILTERS_e3x3 = 128

# fire5 weights and bias
fire5_s1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_s1x1), (FIRE_KERNEL_SIZE_s1x1, FIRE_KERNEL_SIZE_s1x1, CHANNEL, FIRE5_FILTERS_s1x1)))
fire5_s1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE5_FILTERS_s1x1), (FIRE5_FILTERS_s1x1)))
fire5_e1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e1x1), (FIRE_KERNEL_SIZE_e1x1, FIRE_KERNEL_SIZE_e1x1, CHANNEL, FIRE5_FILTERS_e1x1)))
fire5_e1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE5_FILTERS_e1x1), (FIRE5_FILTERS_e1x1)))
fire5_e3x3_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e3x3), (FIRE_KERNEL_SIZE_e3x3, FIRE_KERNEL_SIZE_e3x3, CHANNEL, FIRE5_FILTERS_e3x3)))
fire5_e3x3_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE5_FILTERS_e3x3), (FIRE5_FILTERS_e3x3)))

# fire6 defines
FIRE6_FILTERS_s1x1 = 48
FIRE6_FILTERS_e1x1 = 192
FIRE6_FILTERS_e3x3 = 192

# fire6 weights and bias
fire6_s1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_s1x1), (FIRE_KERNEL_SIZE_s1x1, FIRE_KERNEL_SIZE_s1x1, CHANNEL, FIRE6_FILTERS_s1x1)))
fire6_s1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE6_FILTERS_s1x1), (FIRE6_FILTERS_s1x1)))
fire6_e1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e1x1), (FIRE_KERNEL_SIZE_e1x1, FIRE_KERNEL_SIZE_e1x1, CHANNEL, FIRE6_FILTERS_e1x1)))
fire6_e1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE6_FILTERS_e1x1), (FIRE6_FILTERS_e1x1)))
fire6_e3x3_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e3x3), (FIRE_KERNEL_SIZE_e3x3, FIRE_KERNEL_SIZE_e3x3, CHANNEL, FIRE6_FILTERS_e3x3)))
fire6_e3x3_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE6_FILTERS_e3x3), (FIRE6_FILTERS_e3x3)))

# fire7 defines
FIRE7_FILTERS_s1x1 = 48
FIRE7_FILTERS_e1x1 = 192
FIRE7_FILTERS_e3x3 = 192

# fire7 weights and bias
fire7_s1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_s1x1), (FIRE_KERNEL_SIZE_s1x1, FIRE_KERNEL_SIZE_s1x1, CHANNEL, FIRE7_FILTERS_s1x1)))
fire7_s1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE7_FILTERS_s1x1), (FIRE7_FILTERS_s1x1)))
fire7_e1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e1x1), (FIRE_KERNEL_SIZE_e1x1, FIRE_KERNEL_SIZE_e1x1, CHANNEL, FIRE7_FILTERS_e1x1)))
fire7_e1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE7_FILTERS_e1x1), (FIRE7_FILTERS_e1x1)))
fire7_e3x3_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e3x3), (FIRE_KERNEL_SIZE_e3x3, FIRE_KERNEL_SIZE_e3x3, CHANNEL, FIRE7_FILTERS_e3x3)))
fire7_e3x3_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE7_FILTERS_e3x3), (FIRE7_FILTERS_e3x3)))

# fire8 defines
FIRE8_FILTERS_s1x1 = 64
FIRE8_FILTERS_e1x1 = 256
FIRE8_FILTERS_e3x3 = 256

# fire8 weights and bias
fire8_s1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_s1x1), (FIRE_KERNEL_SIZE_s1x1, FIRE_KERNEL_SIZE_s1x1, CHANNEL, FIRE8_FILTERS_s1x1)))
fire8_s1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE8_FILTERS_s1x1), (FIRE8_FILTERS_s1x1)))
fire8_e1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e1x1), (FIRE_KERNEL_SIZE_e1x1, FIRE_KERNEL_SIZE_e1x1, CHANNEL, FIRE8_FILTERS_e1x1)))
fire8_e1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE8_FILTERS_e1x1), (FIRE8_FILTERS_e1x1)))
fire8_e3x3_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e3x3), (FIRE_KERNEL_SIZE_e3x3, FIRE_KERNEL_SIZE_e3x3, CHANNEL, FIRE8_FILTERS_e3x3)))
fire8_e3x3_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE8_FILTERS_e3x3), (FIRE8_FILTERS_e3x3)))

# fire9 defines
FIRE9_FILTERS_s1x1 = 64
FIRE9_FILTERS_e1x1 = 256
FIRE9_FILTERS_e3x3 = 256

# fire9 weights and bias
fire9_s1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_s1x1), (FIRE_KERNEL_SIZE_s1x1, FIRE_KERNEL_SIZE_s1x1, CHANNEL, FIRE9_FILTERS_s1x1)))
fire9_s1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE9_FILTERS_s1x1), (FIRE9_FILTERS_s1x1)))
fire9_e1x1_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e1x1), (FIRE_KERNEL_SIZE_e1x1, FIRE_KERNEL_SIZE_e1x1, CHANNEL, FIRE9_FILTERS_e1x1)))
fire9_e1x1_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE9_FILTERS_e1x1), (FIRE9_FILTERS_e1x1)))
fire9_e3x3_weights = np.array(np.random.normal(0, np.sqrt(2.0/FIRE_KERNEL_SIZE_e3x3), (FIRE_KERNEL_SIZE_e3x3, FIRE_KERNEL_SIZE_e3x3, CHANNEL, FIRE9_FILTERS_e3x3)))
fire9_e3x3_bias = np.array(np.random.normal(0, np.sqrt(2.0/FIRE9_FILTERS_e3x3), (FIRE9_FILTERS_e3x3)))

def print_structure(weight_file_path):
    """
    Prints out the structure of HDF5 file.

    Args:
      weight_file_path (str) : Path to the file to analyze
    """
    f = h5py.File(weight_file_path, "r")

    bias = []
    weights = []

    try:
        if len(f.attrs.items()):
            print("{} contains: ".format(f.keys()))
            print("Root attributes:")
        for key, value in f.attrs.items():
            print("  {}: {}".format(key, value)) 

        if len(f.items())==0:
            return 

        for layer, g in f.items():
            print("  {}".format(layer))
            print("    Attributes:")
            for key, value in g.attrs.items():
                print("      {}: {}".format(key, value))

            print("    Dataset:")
            for p_name in g.keys():
                param = g[p_name]
                subkeys = param.keys()
                for k_name in param.keys():
                    param2 = param[k_name]
                    #subkeys2 = param2.keys()
                    #print("param.keys(): \n", param.keys())
                    #print("k_name es: \n", k_name)
                    #print("param2.keys(): \n", param2.keys())
                    if ( (k_name == "fire3") or (k_name == "fire2") or (k_name == "fire4") or (k_name == "fire5") or (k_name == "fire6") or (k_name == "fire7") or (k_name == "fire8") or (k_name == "fire9") ):
                        #print("Entreee\n")
                        #print("Struct : \n", layer, g.keys(), param.keys())
                        #print("Entre, keys son: \n", param2.keys())
                        for fire_name in param2.keys():
                            param3 = param2[fire_name]
                            print("         {}: ".format(fire_name))
                            print("             Attributes_2:")
                            print("                 {}/{}: ".format(fire_name, param2.get(fire_name).keys() ))
                            print("             Dataset_2:")
                            for key2 in param3.keys():
                                print("                 {}/{}: {}: ".format( key2, key2, param3.get(key2)[:].shape ))

                            #print("         {}/{}: ".format(fire_name, param2.get(fire_name).keys() ))
                    elif ( (p_name == "conv1") or (p_name == "conv9") ):
                        #print("      {}/{}: {}".format(p_name, k_name, param.get(k_name)[:]))
                        print("      {}/{}: {}".format(p_name, k_name, param.get(k_name)[:].shape ))
                        #print("      {}/{}".format(p_name, k_name ))
    finally:
        f.close()



def create_structure(weight_file_path):
    """
    Prints out the structure of HDF5 file.

    Args:
      weight_file_path (str) : Path to the file to analyze
    """
    f = h5py.File(weight_file_path, "a")

    bias = []
    weights = []
    try:
        f.create_group("conv1")
        f.create_group("pool1")
        f.create_group("fire2")
        f.create_group("fire3")
        f.create_group("fire4")
        f.create_group("pool4") 
        f.create_group("fire5")
        f.create_group("fire6")
        f.create_group("fire7")
        f.create_group("fire8")
        f.create_group("pool8")
        f.create_group("fire9")
        f.create_group("conv9")
        f.create_group("avpool10")
        f.create_group("pred_reshaped")
    except:
        print("Los grupos ya estan creados\n")

    for layer, g in f.items():
        print("Entre a la layer: ", layer)
        print("Tiene estos grupos: ", g)
        try:
            #g.attrs["weight_names"]=[layer+"/kernel", layer+"/bias"]
            if layer=="conv1":
                g.attrs["weight_names"]=[layer+"/kernel", layer+"/bias"]
                g.create_dataset(layer+"/kernel", data=conv1_weights)
                g.create_dataset(layer+"/bias", data=conv1_bias)
            elif layer=="conv9":
                g.attrs["weight_names"]=[layer+"/kernel", layer+"/bias"]
                g.create_dataset(layer+"/kernel", data=convpred_weights)
                g.create_dataset(layer+"/bias", data=convpred_bias)
            elif layer=="fire2":
                g.create_group("expand1x1")
                g.create_group("expand3x3")
                g.create_group("squeeze1x1")
                
                for layer2, g2 in g.items():
                    g2.attrs["weight_names"]=[layer2+"/kernel", layer2+"/bias"]
                    g2.create_group(layer)
                    for layer3, g3 in g2.items():
                        if (layer2 == "expand1x1"):
                            g3.create_dataset(layer2+"/kernel", data=fire2_e1x1_weights)
                            g3.create_dataset(layer2+"/bias", data=fire2_e1x1_bias)
                        elif (layer2 == "expand3x3"):
                            g3.create_dataset(layer2+"/kernel", data=fire2_e3x3_weights)
                            g3.create_dataset(layer2+"/bias", data=fire2_e3x3_bias)
                        elif (layer2 == "squeeze1x1"):
                            g3.create_dataset(layer2+"/kernel", data=fire2_s1x1_weights)
                            g3.create_dataset(layer2+"/bias", data=fire2_s1x1_bias)
            elif layer=="fire3":
                g.create_group("expand1x1")
                g.create_group("expand3x3")
                g.create_group("squeeze1x1")
                
                for layer2, g2 in g.items():
                    g2.attrs["weight_names"]=[layer2+"/kernel", layer2+"/bias"]
                    g2.create_group(layer)
                    for layer3, g3 in g2.items():
                        g3.create_dataset(layer2+"/kernel", data=convpred_weights)
                        g3.create_dataset(layer2+"/bias", data=convpred_bias)
            elif layer=="fire4":
                g.create_group("expand1x1")
                g.create_group("expand3x3")
                g.create_group("squeeze1x1")
                
                for layer2, g2 in g.items():
                    g2.attrs["weight_names"]=[layer2+"/kernel", layer2+"/bias"]
                    g2.create_group(layer)
                    for layer3, g3 in g2.items():
                        g3.create_dataset(layer2+"/kernel", data=convpred_weights)
                        g3.create_dataset(layer2+"/bias", data=convpred_bias)
            elif layer=="fire5":
                g.create_group("expand1x1")
                g.create_group("expand3x3")
                g.create_group("squeeze1x1")
                
                for layer2, g2 in g.items():
                    g2.attrs["weight_names"]=[layer2+"/kernel", layer2+"/bias"]
                    g2.create_group(layer)
                    for layer3, g3 in g2.items():
                        g3.create_dataset(layer2+"/kernel", data=convpred_weights)
                        g3.create_dataset(layer2+"/bias", data=convpred_bias)
            elif layer=="fire6":
                g.create_group("expand1x1")
                g.create_group("expand3x3")
                g.create_group("squeeze1x1")
                
                for layer2, g2 in g.items():
                    g2.attrs["weight_names"]=[layer2+"/kernel", layer2+"/bias"]
                    g2.create_group(layer)
                    for layer3, g3 in g2.items():
                        g3.create_dataset(layer2+"/kernel", data=convpred_weights)
                        g3.create_dataset(layer2+"/bias", data=convpred_bias)
            elif layer=="fire7":
                g.create_group("expand1x1")
                g.create_group("expand3x3")
                g.create_group("squeeze1x1")
                
                for layer2, g2 in g.items():
                    g2.attrs["weight_names"]=[layer2+"/kernel", layer2+"/bias"]
                    g2.create_group(layer)
                    for layer3, g3 in g2.items():
                        g3.create_dataset(layer2+"/kernel", data=convpred_weights)
                        g3.create_dataset(layer2+"/bias", data=convpred_bias)
            elif layer=="fire8":
                g.create_group("expand1x1")
                g.create_group("expand3x3")
                g.create_group("squeeze1x1")
                
                for layer2, g2 in g.items():
                    g2.attrs["weight_names"]=[layer2+"/kernel", layer2+"/bias"]
                    g2.create_group(layer)
                    for layer3, g3 in g2.items():
                        g3.create_dataset(layer2+"/kernel", data=convpred_weights)
                        g3.create_dataset(layer2+"/bias", data=convpred_bias)
            elif layer=="fire9":
                g.create_group("expand1x1")
                g.create_group("expand3x3")
                g.create_group("squeeze1x1")
                
                for layer2, g2 in g.items():
                    g2.attrs["weight_names"]=[layer2+"/kernel", layer2+"/bias"]
                    g2.create_group(layer)
                    for layer3, g3 in g2.items():
                        g3.create_dataset(layer2+"/kernel", data=convpred_weights)
                        g3.create_dataset(layer2+"/bias", data=convpred_bias)


                print("Sali del for \n")
        except:
            print("Los datasets y los labels ya fueron inicializados\n")

        print("Entre a la layer: ", layer)
        print("Tiene estos grupos: ", g)

    #f.create(weight_names)

    f.close()

create_structure(filename)
print_structure(filename)