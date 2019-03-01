import os
from configparser import ConfigParser, ExtendedInterpolation 
from mako.lookup import TemplateLookup

#setup configuration
config = ConfigParser(interpolation = ExtendedInterpolation())
config.read("project.ini")

def renderTemplate(attrib, template):
    
    try:
        tmp_lookup = TemplateLookup(attrib['tmp_dir'])
        tmp = tmp_lookup.get_template(template)
        
        file_dir = os.path.join(attrib['tmp_write_dir'], attrib['filename'])
        
        with open(file_dir, 'w', newline = '') as fTmp:
            fTmp.write(tmp.render(data=attrib))
            
    except Exception as e:
        print(e)


def get_src_files(src_dir, cc_type):
    
    src_files = []
    
    list_root = []
    list_dirs = []
    
    if cc_type == "g++":
        file_ext = ".cpp"
    elif cc_type == "gcc":
        file_ext = ".c"
    else:
        file_ext = ".xyz" 
    
    try:
        for root, dirs, files in os.walk(src_dir):
            if not files == []:                                
                for item in files:
                    if item.endswith(file_ext):
                        if root == src_dir:
                            src_files.append(item)
                        else:
                            rpath = root[root.find(src_dir)+len(src_dir)+1:]
                            src_files.append(rpath + "/" + item)
                        
    except Exception as e:
        print(e)
        
    return src_files
    

def get_include_dir(dictINCS):
    
    list_inc_dir = []
    
    for key, value in dictINCS.items():
        if not key == "root_dir":
            list_inc_dir.append(value)
        
    return list_inc_dir

def get_libs(dictLIBS):
        
    list_libs = dictLIBS['libs'].split(",")
    
    return list_libs

def get_lib_paths(dictLIBPATHS):
    
    list_lib_dir = []
    
    for key, value in dictLIBPATHS.items():
        if not key == "root_dir":
            list_lib_dir.append(value)
        
    return list_lib_dir


def main():
    dictPRJ = dict(config['PROJECT']) 
    dictDIR = dict(config['DIRECTORIES'])
    dictCOMP = dict(config['COMPILER'])    
    dictINCS = dict(config['INCLUDES'])
    dictLIBS = dict(config['LIBRARIES'])
    dictLIBPATHS = dict(config['LIBRARY_PATHS'])        
    
    attrib = {}
    attrib['prj_name'] = dictPRJ['name']
    attrib['cc'] = dictCOMP['cc']
    attrib['cflags'] = dictCOMP['cflags']    
    attrib['includes'] = get_include_dir(dictINCS)
    attrib['lflags'] = get_lib_paths(dictLIBPATHS)
    attrib['libs'] = get_libs(dictLIBS)
    attrib['srcs'] = get_src_files(dictDIR['src_dir'], dictCOMP['cc'])
    attrib['tmp_dir'] = dictDIR['tmp_dir']    
    attrib['tmp_write_dir'] = dictDIR['src_dir']
    attrib['filename'] = "Makefile"
    
    renderTemplate(attrib, "Makefile_tmp")
    
if __name__ == '__main__':    
   
    main()
    
     
                    
            