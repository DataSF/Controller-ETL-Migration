

#!/bin/bash
#
#bash script to run a particular python job, using a python path and config files


OPTIND=1         # Reset in case getopts has been used previously in the shell.
display_help() {
    echo
    echo "Usage: $0 [option...] {d}" >&2
    echo
    echo "   -d, --main_dir   -- main path to package files"
    echo
    echo "   -c, --config_file_for_job   ---   run the script to update asset fields using this config file"
    echo
    echo "   -p, --python_path  -- path to python- ie run which python to find out"
    echo
    echo "   -h,  --help enter -h to display this help message"
    echo
    echo "  EX: ./run_job_update_profiles.sh -d /Users/j9/Desktop/datasf-profiler/ -c fieldConfig_profiler_desktop.yaml -p /usr/local/bin/python -t Y -f Y -m Y  "
    echo
    echo "   -j, --job_name  -- name_of_python_file_to_run " 
    echo
    exit 1
}


# Initialize our own variables:
path_to_main_dir=""
config_fn=""
python_path=""
job_name=""

while getopts "h?:d:c:p:j:m:" opt; do
    case "$opt" in
    h|\?)
        display_help
        exit 0
        ;;
    d)  path_to_main_dir=$OPTARG
        ;;
    c)  config_fn=$OPTARG
        ;;
    p)  python_path=$OPTARG
        ;;
    j) python_file_to_run=$OPTARG
    esac
done

shift $((OPTIND-1))



#[ "$1" = "--" ] && shift
if [ -z "$path_to_main_dir" ]; then
    echo
    echo "*****You must enter a path to the main directory****"
    display_help
    exit 1
fi
if [ -z "$config_fn" ]; then
    echo
    echo "*****You must enter a config file to run the job****"
    display_help
    exit 1
fi
if [ -z "$python_path" ]; then
    echo "*****You must enter a path for python****"
    display_help
    exit 1
fi
if [ -z "$python_file_to_run" ]; then
    echo "*****You must enter a python file to run****"
    display_help
    exit 1
fi


config="configs/"
config_dir=$path_to_main_dir$config


#run the job
$python_path $path_to_main_dir$python_file_to_run -c $config_fn -d $config_dir

