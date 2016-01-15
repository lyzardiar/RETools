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

using PublicTools.View;

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
        }

        private void PNGDropContent_Drop(object sender, DragEventArgs e)
        {
            System.Array array = ((System.Array)e.Data.GetData(DataFormats.FileDrop));
            bool? isOverlap = CBIsOverlap.IsChecked;
            PNGEncodeView.Instance.workWithFileList(array, isOverlap.Value);
        }
    }
}
