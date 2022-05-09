import h5py
import numpy as np

filename = "imagenet.h5"



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
                    if ( (k_name == "fire3") or (k_name == "fire2") or (k_name == "fire4") or (k_name == "fire5") or (k_name == "fire6") or (k_name == "fire7") or (k_name == "fire8") or (k_name == "fire9") ):
                        #print("Struct : \n", layer, g.keys(), param.keys())
                        for fire_name in param2.keys():
                            param3 = param2[fire_name]
                            print("         {}: ".format(fire_name))
                            print("             Attributes_2:")
                            print("                 {}/{}: ".format(fire_name, param2.get(fire_name).keys() ))
                            print("             Dataset_2:")
                            for key2 in param3.keys():
                                print("                 {}/{}: {}: ".format( key2, key2, param3.get(key2)[:].shape ))

                            #print("         {}/{}: ".format(fire_name, param2.get(fire_name).keys() ))
                    elif ( (p_name == "conv12") or (p_name == "conv2d_1") ):
                        #print("      {}/{}: {}".format(p_name, k_name, param.get(k_name)[:]))
                        print("      {}/{}: {}".format(p_name, k_name, param.get(k_name)[:].shape ))
                        #print("      {}/{}".format(p_name, k_name ))
    finally:
        f.close()


print_structure(filename)