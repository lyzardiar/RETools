using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PublicTools
{
    public class FileHelper
    {
        /// <summary>
        /// 获取给定目录下的所有文件名
        /// </summary>
        /// <param name="dirpath"></param>
        /// <param name="inList"></param>
        /// <returns>List<string></returns>
        public static List<string> walkDir(string dirpath, List<string> inList = null)
        {
            List<string> ret = inList;
            if (ret == null)
                ret = new List<string>();

            if (System.IO.Directory.Exists(dirpath))
            {
                System.IO.Directory.GetFiles(dirpath);
                ret.AddRange(System.IO.Directory.EnumerateFiles(dirpath));

                foreach (string path in System.IO.Directory.EnumerateDirectories(dirpath))
                {
                    walkDir(path, ret);
                }
            }
            else
            {
                ret.Add(dirpath);
            }

            return ret;
        }
    }
}
