using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace PublicTools.Helper
{
    public class PNGEncodeHelper : BaseHelper
    {
        static PNGEncodeHelper _instance;
        public static PNGEncodeHelper Instance
        {
            get
            {
                if (_instance == null)
                    _instance = new PNGEncodeHelper();
                return _instance;
            }
        }

        public enum ConvertType
        {
            ETC,
            JPGA,
            PVR,
            PVRTC4
        };
        public ConvertType convertType = ConvertType.ETC;

        string getToolPath(ConvertType type)
        {
            string ret = "";
            switch (type)
            {
                case ConvertType.ETC:
                    ret = System.IO.Path.Combine(Global.toolsDir, "PackImg2Mng.py");
                    break;
                case ConvertType.JPGA:
                    break;
                case ConvertType.PVR:
                    break;
                case ConvertType.PVRTC4:
                    break;

            }
            return ret;
        }

        public override void workWithFileList(System.Array arr, bool isOverlap = true)
        {
            string executeFilePath;
            string param = getToolPath(convertType) + " ";

            List<string> paths = new List<string>();
            foreach (String path in arr)
            {
                param += " -d " + path;
            }

            executeFilePath = @"python.exe";
            Global.execute(executeFilePath, param);
        }

        public override bool work(List<string> paths, bool isOverlap)
        {
            foreach (string path in paths)
                Global.updateDescription(path);
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
                Global.execute(executeFilePath, param);
            }
        }

    }
}
