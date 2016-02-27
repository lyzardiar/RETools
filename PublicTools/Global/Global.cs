using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

using System.Windows.Controls;
using System.Threading;

namespace PublicTools
{
    public class Global
    {
        static bool isLocked = false;
        static Process curProcess = null;

        public static TextBox stateLabel = null;
        public static SynchronizationContext syncContext = null;

        static string _androidBuildPath = @"E:\Workspace\Mobilephone_DDT\trunk\Client\Engine\proj.android\build_native.py ";
        public static string androidBuildPath
        {
            get{ return _androidBuildPath; }
            set { _androidBuildPath = value; }
        }

        public static string appPath
        {
            get
            {
                return System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName;
            }
        }

        public static string appDir
        {
            get
            {
                string path = System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName;
                return System.IO.Path.GetDirectoryName(path);
            }
        }

        public static string toolsDir
        {
            get
            {
                string path = System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName;
                path = System.IO.Path.Combine(System.IO.Path.GetDirectoryName(path), "../tools");
                return path;
            }
        }

        public static string svnDiffHelper
        {
            get
            {
                string path = System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName;
                path = System.IO.Path.Combine(System.IO.Path.GetDirectoryName(path), "../tools/svnDiffHelper.py");
                return path;
            }
        }

        public static void execute(string filePath, string param)
        {
            if (isLocked)
            {
                updateDescription("有任务正在执行, 请稍后重试!!!!");
                return;
            }

            Global.stateLabel.Clear(); 

            updateDescription("执行文件: " + filePath);
            updateDescription("执行参数: " + param);
            updateDescription("输出:");

            Task t = new Task(() => {
                execute_Task(filePath, param);
            });
            t.Start();
            isLocked = true;
            t.ContinueWith(task => {
                updateDescription("任务执行完成!!!!!!!");
                curProcess = null;
                isLocked = false;
            });
        }

        static void execute_Task(string filePath, string param)
        {
            Process myProcess = new Process();
            ProcessStartInfo myProcessStartInfo = new ProcessStartInfo("\"" + filePath + "\"", param);
            myProcess.StartInfo = myProcessStartInfo;
            myProcess.StartInfo.UseShellExecute = false;
            myProcess.StartInfo.RedirectStandardOutput = true;
            myProcess.StartInfo.RedirectStandardInput = true;
            myProcess.StartInfo.RedirectStandardError = true;
            myProcess.StartInfo.CreateNoWindow = true;
            myProcess.OutputDataReceived += (sender, data) =>
            {
                try
                {
                    updateDescription(data.Data);
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.Data);
                }
            };
            myProcess.Start();
            curProcess = myProcess;

            myProcess.BeginOutputReadLine();
            myProcess.WaitForExit();
            myProcess.Close();
        }

        public static void updateDescription(object msg)
        {
            if (msg != null)
            {
                //Console.WriteLine(msg);
                syncContext.Post(updateDescription_, msg);
            }
        }

        static void updateDescription_(object msg)
        {
            Global.stateLabel.AppendText(msg.ToString() + Environment.NewLine);
            Global.stateLabel.ScrollToEnd();
        }
    }
}
