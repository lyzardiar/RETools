using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

using PublicTools.Helper;
using System.Threading;
using Microsoft.Win32;

namespace PublicTools
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();

            Global.stateLabel = stateLabel;
            stateLabel.Text = "";
            stateLabel.IsReadOnly = true;

            Global.syncContext = SynchronizationContext.Current;
            androidProjDir.Text = Global.androidBuildPath;
        }

        private void PNGDropContent_Drop(object sender, DragEventArgs e)
        {
            System.Array array = ((System.Array)e.Data.GetData(DataFormats.FileDrop));
            bool isOverlap = CBIsOverlap.IsChecked.Value;
            bool isETCEncode = ETCEncodeTag.IsChecked.Value;
            bool isJPGAEncode = JPGAEncodeTag.IsChecked.Value;
            bool isPVREncode = PVREncodeTag.IsChecked.Value;
            bool isPVRTC4Encode = PVRTC4EncodeTag.IsChecked.Value;

            PNGEncodeHelper.Instance.isFast = pngIsFast.IsChecked.Value;

            if (isETCEncode)
            {
                PNGEncodeHelper.Instance.convertType = PNGEncodeHelper.ConvertType.ETC;
            }
            else if (isJPGAEncode)
            {
                PNGEncodeHelper.Instance.convertType = PNGEncodeHelper.ConvertType.JPGA;
            }
            else if (isPVREncode)
            {
                PNGEncodeHelper.Instance.convertType = PNGEncodeHelper.ConvertType.PVR;
            }
            else if (isPVRTC4Encode)
            {
                PNGEncodeHelper.Instance.convertType = PNGEncodeHelper.ConvertType.PVRTC4;
            }
            PNGEncodeHelper.Instance.workWithFileList(array, isOverlap);
        }

        private void androidPublicBtn_Click(object sender, RoutedEventArgs e)
        {
            bool isClean = CleanTag.IsChecked.Value;
            bool isAddVersion = AddVersionTag.IsChecked.Value;
            bool isDebug = DebugTag.IsChecked.Value;
            bool isNativeBuild = NativeBuildTag.IsChecked.Value;
            bool isPackApk = PackApkTag.IsChecked.Value;
            bool isPackSymbols = PackSymbolsTag.IsChecked.Value;

            string executeFilePath;
            string param = Global.androidBuildPath;

            string c = isClean ? " -c" : " -C";
            string v = isAddVersion ? " -v 1" : " -v 0";
            string m = isDebug ? " -m debug" : " -m release";
            string n = isNativeBuild ? " -n" : " -N";
            string a = isPackApk ? " -a" : " -A";
            string s = isPackSymbols ? " -s" : " -S";

            param = param + c + v + m + n + a + s;

            executeFilePath = @"python.exe";
            Global.execute(executeFilePath, param);
        }

        private void selectAndroidProjDirBtn_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Filter = "(*.py)|*.py";
            if (ofd.ShowDialog().Value)
            {
                string fileName = ofd.FileName;
                androidProjDir.Text = fileName;
                Global.androidBuildPath = fileName;
            }
        }

        private void clearBtn_Click(object sender, RoutedEventArgs e)
        {
            stateLabel.Text = "";
        }
    }
}
