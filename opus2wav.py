import os
import subprocess
import sys
from pathlib import Path

def convert_opus_to_wav(input_file, output_dir=None, force_wav=True, quiet=False):
    """
    使用opusdec将单个Opus/OGG文件转换为WAV
    
    参数:
        input_file: 输入文件路径
        output_dir: 输出目录(默认为输入文件所在目录)
        force_wav: 强制使用WAV格式(即使扩展名不是.wav)
        quiet: 是否抑制程序输出
    """
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"错误: 文件不存在 {input_file}", file=sys.stderr)
        return False
    
    # 确定输出目录
    if output_dir is None:
        output_dir = input_path.parent
    else:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 构造输出文件名
    output_file = input_path.with_suffix('.wav')
    if force_wav:
        output_file = output_dir / f"{input_path.stem}.wav"
    
    # 构建opusdec命令
    cmd = ['opusdec.exe']
    if force_wav:
        cmd.append('--force-wav')
    if quiet:
        cmd.append('--quiet')
    cmd.extend([str(input_path), str(output_file)])
    
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE if quiet else None)
        print(f"转换成功: {input_file} -> {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {input_file} (错误码: {e.returncode})", file=sys.stderr)
        return False
    except Exception as e:
        print(f"处理 {input_file} 时发生意外错误: {str(e)}", file=sys.stderr)
        return False

def batch_convert_opus_to_wav(input_files, output_dir=None, force_wav=True, quiet=False):
    """
    批量转换Opus/OGG文件为WAV
    
    参数:
        input_files: 输入文件列表(可以是文件或目录)
        output_dir: 输出目录
        force_wav: 强制使用WAV格式
        quiet: 是否抑制程序输出
    """
    converted = 0
    failed = 0
    
    for input_item in input_files:
        input_path = Path(input_item)
        
        if input_path.is_dir():
            # 处理目录中的所有Opus/OGG文件
            for file_path in input_path.glob('**/*'):
                if file_path.suffix.lower() in ('.opus', '.ogg'):
                    if not convert_opus_to_wav(file_path, output_dir, force_wav, quiet):
                        failed += 1
                    converted += 1
        elif input_path.is_file() and input_path.suffix.lower() in ('.opus', '.ogg'):
            # 处理单个文件
            if not convert_opus_to_wav(input_path, output_dir, force_wav, quiet):
                failed += 1
            converted += 1
        else:
            print(f"警告: 跳过不支持的路径 {input_item}", file=sys.stderr)
    
    print(f"\n转换完成: 成功 {converted - failed} 个, 失败 {failed} 个")
    return converted - failed, failed

def main():
    # 检查opusdec.exe是否存在在当前目录中
    if not os.path.exists('opusdec.exe'):
        #print("错误: opusdec.exe未找到", file=sys.stderr)
        # 切换到当前目录
        #print('正在尝试从当前目录查找opusdec.exe...')
        #os.chdir(os.path.dirname(__file__))
        # 更改cmd命令为当前路径/opusdec.exe
        
        #if not os.path.exists('opusdec.exe'):
        print("错误: opusdec.exe未找到", file=sys.stderr)
        sys.exit(1)
    

    import argparse
    
    parser = argparse.ArgumentParser(
        description='批量将Opus/OGG音频文件转换为WAV格式',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input', nargs='+', help='输入文件或目录(支持通配符)')
    parser.add_argument('-o', '--output-dir', help='输出目录(默认为输入文件所在目录)')
    parser.add_argument('--no-force-wav', dest='force_wav', action='store_false',
                        help='不强制使用WAV格式(使用原始扩展名)')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='抑制程序输出')
    
    args = parser.parse_args()
    
    # 扩展通配符路径
    expanded_inputs = []
    for path in args.input:
        expanded_inputs.extend(glob.glob(path, recursive=True))
    
    if not expanded_inputs:
        print("错误: 没有找到匹配的输入文件", file=sys.stderr)
        sys.exit(1)
    
    success, failed = batch_convert_opus_to_wav(
        expanded_inputs,
        args.output_dir,
        args.force_wav,
        args.quiet
    )
    
    if failed > 0:
        sys.exit(1)

if __name__ == '__main__':
    # 需要导入glob用于通配符扩展
    import glob
    main()