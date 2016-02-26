// MPConvert.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "MPInfo.h"

struct CMDInfo
{
	char ch;
};

string excpath;

const char* jpgcmd ="%sconvert.exe \"%s\" -quality 65%% -background black \"%s\" ";
const char* alphacmd ="%sconvert.exe \"%s\" -quality 75%% -channel A -alpha extract \"%s\" ";

char pngPath[256];
char jpgPath[256];
char alphaPath[256];
char cmdStr[1024];

void convertPNG2JPG(string imgpath, int pngCnt)
{
	for (int i = 0; i < pngCnt; ++i)
	{
		sprintf(pngPath, "%s%d_%d.png", imgpath.c_str(), 0, i);
		sprintf(jpgPath, "%s%d_%d.jpg", imgpath.c_str(), 0, i);
		sprintf(alphaPath, "%s%d_%d.alpha.jpg", imgpath.c_str(), 0, i);

		sprintf(cmdStr, jpgcmd, excpath.c_str(), pngPath, jpgPath);
		system(cmdStr);

		sprintf(cmdStr, alphacmd, excpath.c_str(), pngPath, alphaPath);
		system(cmdStr);

		sprintf(cmdStr, "%s", pngPath);
		remove(cmdStr);

		rename(jpgPath, pngPath);
		remove(jpgPath);

		sprintf(cmdStr, "%s%d_%d.png.alpha", imgpath.c_str(), 0, i);
		rename(alphaPath, cmdStr);
		remove(alphaPath);
	}
}

void convertPNG2ETC(string imgpath, int pngCnt)
{
	for (int i = 0; i < pngCnt; ++i)
	{
		sprintf(pngPath, "%s%d_%d.png", imgpath.c_str(), 0, i);
		sprintf(cmdStr, "python %sPackImg2Mng.py -d %s", excpath.c_str(), pngPath);
		system(cmdStr);
	}
}

void packageMP1(MPReader& reader, int pngCnt)
{
	MPWriter w(reader.path.c_str());

	auto imgpath = reader.imagePath;

	w.writeByte(0);
	w.writeByte(0);
	w.writeByte(0);
	w.writeByte(1);

	w.writeByte(2);

	w.writeByte(2);
	w.writeByte(pngCnt);
	for (int i = 0; i < pngCnt; ++i)
	{
		sprintf(jpgPath, "%s%d_%d.png", imgpath.c_str(), 0, i);

		FileState jpgInfo(jpgPath); 

		w.writeInt(jpgInfo.size);
		w.writeBytes(jpgInfo.data, jpgInfo.size);

		remove(jpgPath);
	}

	sprintf(cmdStr, "%s_%d.json", imgpath.c_str(), 0);
	FileState mcInfo(cmdStr); 
	w.writeInt(mcInfo.size);
	w.writeBytes(mcInfo.data, mcInfo.size);
	remove(cmdStr);
	
	sprintf(cmdStr, "%s_%d.info", imgpath.c_str(), 0);
	FileState iInfo(cmdStr); 
	w.writeInt(iInfo.size);
	w.writeBytes(iInfo.data, iInfo.size);
	remove(cmdStr);
}

void packageMP2(MPReader& reader, int pngCnt)
{
	MPWriter w(reader.path.c_str());

	auto imgpath = reader.imagePath;

	w.writeByte(0);
	w.writeByte(0);
	w.writeByte(0);
	w.writeByte(1);

	w.writeByte(3);

	sprintf(cmdStr, "%s_%d.act", imgpath.c_str(), 0);
	FileState actInfo(cmdStr); 
	w.writeBytes(actInfo.data, actInfo.size);
	remove(cmdStr);

	sprintf(cmdStr, "%s_%d.json", imgpath.c_str(), 0);
	FileState mcInfo(cmdStr); 
	w.writeInt(mcInfo.size);
	w.writeBytes(mcInfo.data, mcInfo.size);
	remove(cmdStr);

	w.writeByte(2);
	w.writeByte(pngCnt);
	for (int i = 0; i < pngCnt; ++i)
	{
		sprintf(jpgPath, "%s%d_%d.png", imgpath.c_str(), 0, i);

		FileState jpgInfo(jpgPath); 

		w.writeInt(jpgInfo.size);
		w.writeBytes(jpgInfo.data, jpgInfo.size);

		remove(jpgPath);
	}

	sprintf(cmdStr, "%s_%d.info", imgpath.c_str(), 0);
	FileState iInfo(cmdStr); 
	w.writeInt(iInfo.size);
	w.writeBytes(iInfo.data, iInfo.size);
	remove(cmdStr);
}

bool convertMp(const char* filepath)
{
	MPReader reader(filepath);

	MPHeader header(reader);
	
	int mpType = 0;
	int pngCnt = 0;
	for (int i = 0; i < header.mpCnt; ++i)
	{
		char nMCType = reader.readByte(); // 文件类型  1=plist 2=mc 3=mc2
		switch (nMCType)
		{
		case 1:
			break;
		case 2:
			pngCnt = MP1Reader::load(reader, reader.imagePath, i);
			mpType = 1;
			break;
		case 3:
			pngCnt = MP2Reader::load(reader, reader.imagePath, i);
			mpType = 2;
			break;
		default:
			break;
		}

		// Only support single mp
		break;
	}

	if (pngCnt > 0)
	{
		convertPNG2ETC(reader.imagePath, pngCnt);
		sprintf(cmdStr, "%s.mp", reader.imagePath.c_str());
		remove(cmdStr);

		if (mpType == 1)
			packageMP1(reader, pngCnt);
		if (mpType == 2)
			packageMP2(reader, pngCnt);
	}

	sprintf(cmdStr, "%s_%d.act", reader.imagePath.c_str(), 0);
	remove(cmdStr);

	sprintf(cmdStr, "%s_%d.json", reader.imagePath.c_str(), 0);
	remove(cmdStr);
	return true;
}

char* ConvertLPWSTRToLPSTR (LPWSTR lpwszStrIn)  
{  
	LPSTR pszOut = NULL;  
	if (lpwszStrIn != NULL)  
	{  
		int nInputStrLen = wcslen (lpwszStrIn);  

		// Double NULL Termination   
		int nOutputStrLen = WideCharToMultiByte (CP_ACP, 0, lpwszStrIn, nInputStrLen, NULL, 0, 0, 0) + 2;  
		pszOut = new char [nOutputStrLen];  

		if (pszOut)  
		{  
			memset (pszOut, 0x00, nOutputStrLen);  
			WideCharToMultiByte(CP_ACP, 0, lpwszStrIn, nInputStrLen, pszOut, nOutputStrLen, 0, 0);  
		}  
	}  
	return pszOut;  
}  

int _tmain(int argc, _TCHAR* argv[])
{
	TCHAR szFilePath[MAX_PATH + 1]={0};
	GetModuleFileName(NULL, szFilePath, MAX_PATH);
	(_tcsrchr(szFilePath, _T('\\')))[1] = 0; // 删除文件名，只获得路径字串

	excpath = ConvertLPWSTRToLPSTR(szFilePath);

	if (argc > 1)
	{
		for (int i = 1; i < argc; ++i)
		{
			char* path = ConvertLPWSTRToLPSTR(argv[i]);
			convertMp(path);
		}
	}
	return 0;
}

