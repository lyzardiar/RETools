using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SharpSvn;
using SharpSvn.Security;

namespace PublicTools.Helper
{
    public class SVNHelper
    {
        public static void getDiff(int lastVersion)
        {
            using (SvnClient client = new SvnClient())
            {
                client.Authentication.UserNamePasswordHandlers +=
                    new EventHandler<SvnUserNamePasswordEventArgs>(
                        delegate (object s, SvnUserNamePasswordEventArgs e)
                        {
                            e.UserName = "yun.bo";
                            e.Password = "boyun";
                        });
                SvnInfoEventArgs clientInfo;
                string path = @"http://test10.svn.7road-inc.com/svn/Mobilephone_SRC/Mobilephone_DDT/trunk/Client/Develop/Resource";
                
                client.GetInfo(path, out clientInfo);

                int i = 0;
            }
        }

    }
}
