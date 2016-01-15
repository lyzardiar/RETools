using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PublicTools.View
{
    public class BaseView
    {
        List<string> iterDir(String dirpath, List<string> inList = null)
        {
            List<string> ret = inList;
            if (ret == null)
                ret = new List<string>();

            if (System.IO.Directory.Exists(dirpath))
            {
                System.IO.Directory.GetFiles(dirpath);
                ret.AddRange(System.IO.Directory.EnumerateFiles(dirpath));

                foreach (String path in System.IO.Directory.EnumerateDirectories(dirpath))
                {
                    iterDir(path, ret);
                }
            }
            else
            {
                ret.Add(dirpath);
            }

            return ret;
        }

        public void workWithFileList(System.Array arr, bool isOverlap = true)
        {
            List<string> paths = new List<string>();
            foreach (String path in arr)
            {
                // 文件夹
                if (System.IO.Directory.Exists(path))
                {
                    paths.AddRange(iterDir(path));
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
