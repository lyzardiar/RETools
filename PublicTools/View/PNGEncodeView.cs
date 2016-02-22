using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace PublicTools.View
{
    public class PNGEncodeView : BaseView
    {
        static PNGEncodeView _instance;
        public static PNGEncodeView Instance
        {
            get
            {
                if (_instance == null)
                    _instance = new PNGEncodeView();
                return _instance;
            }
        }

        public override bool work(List<string> paths, bool isOverlap)
        {
            foreach (string path in paths)
                updateDescription(path);
            return true;
        }

        //加密图片
        public void encodeImage(string inputPath, string outputPath)
        {
            if (System.IO.Directory.Exists(inputPath) || System.IO.File.Exists(inputPath))
            {
                string executeFilePath;
                string param;
                executeFilePath = System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName;
                executeFilePath = System.IO.Path.GetDirectoryName(executeFilePath);
                executeFilePath = executeFilePath + @"\encodeTools\PngEncode.exe";
                param = "-i " + "\"" + inputPath + "\"" + " -o " + "\"" + outputPath + "\"";
                executeFile(executeFilePath, param);
            }
        }

        void executeFile(string filePath, string param)
        {
            updateDescription("执行文件: " + filePath);
            updateDescription("执行参数: " + param);
            updateDescription("输出:");
            Process myProcess = new Process();
            ProcessStartInfo myProcessStartInfo = new ProcessStartInfo("\"" + filePath + "\"", param);
            myProcess.StartInfo = myProcessStartInfo;
            myProcess.StartInfo.UseShellExecute = false;
            myProcess.StartInfo.RedirectStandardOutput = true;
            myProcess.Start();
            while (!myProcess.HasExited)
            {
                updateDescription(myProcess.StandardOutput.ReadToEnd());
                myProcess.WaitForExit();
            }
            myProcess.Close();
        }

        public void updateDescription(string msg)
        {
            Global.stateLabel.Text += msg + "\n";
        }
    }
}
