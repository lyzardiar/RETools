using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PublicTools.Helper
{
    public class BaseHelper
    {
        public virtual void workWithFileList(System.Array arr, bool isOverlap = true)
        {
            List<string> paths = new List<string>();
            foreach (String path in arr)
            {
                // 文件夹
                if (System.IO.Directory.Exists(path))
                {
                    paths.AddRange(FileHelper.walkDir(path));
                }
                else if (System.IO.File.Exists(path))
                {
                    paths.Add(path);
                }
            }
            work(paths, isOverlap);
        }

        public virtual bool work(List<string> paths, bool isOverlap)
        {
            return true;
        }
    }
}
