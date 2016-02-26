#pragma once
#include <winsock2.h>
#include <io.h>
#pragma   comment(lib,"Ws2_32.lib")

#include <stdio.h>
#include <string>

using namespace std;

struct FileState
{
	FileState(const char* filepath)
	{
		FILE* fp;
		fopen_s(&fp, filepath, "rb");
		fseek(fp, 0, SEEK_END);
		size = ftell(fp);

		fseek(fp, 0, SEEK_SET);
		data = new unsigned char[size + 1];
		size = fread(data, sizeof(unsigned char), size, fp);
		data[size] = 0;
		fclose(fp);
	}

	~FileState()
	{
		delete [] data;
	}

	int size;
	unsigned char* data;
};

struct MPWriter {
	MPWriter(const char* filepath)
	{
		path = filepath;
		fopen_s(&fp, filepath, "wb+");
	}
	~MPWriter(){
		fclose(fp);
	}

	void writeByte(unsigned char byte){
		fwrite(&byte, 1, 1, fp);
	}

	void writeBytes(unsigned char* bytes, int len){
		fwrite(bytes, 1, len, fp);
	}

	void writeInt(int val){
		val = ntohl(*((int*)(&val)));
		fwrite(&val, 4, 1, fp);
		
	}

	void writeShort(short val){
		val = ntohs(*((short*)(&val)));
		fwrite(&val, 2, 1, fp);
	}

	void writeFloat(float val){
		val = ntohl(*((int*)(&val)));
		fwrite(&val, 4, 1, fp);
	}

	string path;
	FILE* fp;
};

struct MPReader{
	MPReader(const char* filepath)
	{
		path = filepath;

		imagePath = path;
		size_t startPos = imagePath.find_last_of("."); 	
		imagePath = imagePath.erase(startPos);
		
		FILE* fp;
		fopen_s(&fp, filepath, "rb");

		fseek(fp, 0, SEEK_END);
		auto size = ftell(fp);
		fseek(fp, 0, SEEK_SET);
		data = new unsigned char[size + 1];

		size = fread(data, sizeof(unsigned char), size, fp);
		data[size] = 0;
		fclose(fp);

		position = 0;
	}

	~MPReader(){
		//CC_SAFE_FREE(data);
	}
	
	void seek(int len = 1) { position += len; }
	unsigned char readByte() { return data[position++]; }
	int readInt() { int ret = ntohl(*((int*)(data+position))); position+=4; return ret; }
	short readShort() { int ret = ntohs(*((short*)(data+position))); position+=2; return ret; }
	float readFloat() {
		float ret = 0;
		ret = (float)ntohl(*((int*)data));
		position+=4; 
		return ret; 
	}
	unsigned char* readBytes(int len) { unsigned char* ret = data + position; position += len; return ret; }

	bool write(int len, const char* filepath)
	{
		FILE* fp;
		fopen_s(&fp, filepath, "wb+");
		fwrite(data + position, 1, len,fp);
		position += len;
		fclose(fp);
		return true;
	}

	void reset() { position = 0; }

	unsigned int position;
	unsigned char* data;
	string path, imagePath;
	int size;
};

struct MPHeader {
	char topLen; // 头部大小
	char sType	; // 加密类型  0=null
	char rType	; // 压缩类型  0=null 1=zlib 2=zip 3=7z
	char mpCnt	; // 动画个数

	MPHeader()
		: topLen(0)
		, sType (0)
		, rType (0)
		, mpCnt (0)
	{

	}

	MPHeader(MPReader& reader)
	{
		read(reader);
	}

	bool read(MPReader& reader) 
	{
		topLen	= reader.readByte();
		sType	= reader.readByte();
		rType	= reader.readByte();
		mpCnt	= reader.readByte();
		return true;
	}
};

struct MP1Reader {
	static int load(MPReader& reader, string szMPImgPath, int index)
	{
		std::string imgTail;
		char szImgPath[256];
		char nResType = reader.readByte(); // 资源类型 1=pvr 2=png 3=jpg 4=pvr.ccz 5=ppm 6=dxt1 7=dxt2 8=dxt3 9=dxt4 10=dxt5 11=tga 12=webp
		switch (nResType)
		{
		case 1:
			imgTail = "pvr";
			break;
		case 2:
			imgTail = "png";
			break;
		case 3:
			imgTail = "jpg";
			break;
		case 4:
			imgTail = "pvr.ccz";
			break;
		case 5:
			imgTail = "ppm";
			break;
		case 12:
			imgTail = "webp";
			break;
		case 16:
			return 0;
			break;
		default:
			break;
		}
		char nPicCnt = reader.readByte(); // 图片资源数目
		// 读取并加载所有图片资源
		for (int nPicIdx = 0; nPicIdx < nPicCnt; ++nPicIdx)
		{
			int nPicLen = reader.readInt();
			sprintf(szImgPath, "%s%d_%d.%s", szMPImgPath.c_str(), index, nPicIdx, imgTail.c_str());
			reader.write(nPicLen, szImgPath);
		}

		// 读取MC数据
		int nMCLen = reader.readInt();
		sprintf(szImgPath, "%s_%d.json", szMPImgPath.c_str(), index);
		reader.write(nMCLen, szImgPath);

		int infolen = 0;
		char nParamNum = reader.readByte();
		infolen ++;
		const unsigned char* pParamStart = reader.readBytes(nParamNum);
		infolen += nParamNum;
		for(int j = 0; j < nParamNum; j++)
		{
			char nParam = pParamStart[j];
			switch (nParam)
			{
			case 0:
				{		
					// 读取mc位置信息
					short nPosX = reader.readShort();
					short nPosY = reader.readShort();
					infolen += 4;
					break;
				}
			case 1:
				{
					float fRotation = reader.readFloat();
					infolen += 4;
					break;
				}
			case 2:
				{
					float fScaleX = reader.readFloat();
					float fScaleY = reader.readFloat();
					infolen += 8;
					break;
				}
			default:
				break;
			}
		}

		// 存储MC信息
		sprintf(szImgPath, "%s_%d.info", szMPImgPath.c_str(), index);
		reader.seek(-infolen);
		reader.write(infolen, szImgPath);
		return nPicCnt;
	}

};

struct MP2Reader {
	static int load(MPReader& reader, string szMPImgPath, int index)
	{
		char szImgPath[256];

		int len = 0;
		int tag = reader.readInt();
		len += 4;
		int actionCount = reader.readByte();
		len += 1;
		for (int i = 0; i < actionCount; ++i)
		{
			int nameLen = reader.readInt();
			len += 4;
			string name((char*)reader.readBytes(nameLen), nameLen);
			len += nameLen;
			int picIndexCount = reader.readByte();
			len += 1;
			for (int j = 0; j < picIndexCount; ++j)
			{
				reader.readByte();
				len += 1;
			}
		}
		// 存储MC2act信息
		sprintf(szImgPath, "%s_%d.act", szMPImgPath.c_str(), index);
		reader.seek(-len);
		reader.write(len, szImgPath);

		// 读取MC数据
		int nMCLen = reader.readInt();
		sprintf(szImgPath, "%s_%d.json", szMPImgPath.c_str(), index);
		reader.write(nMCLen, szImgPath);

		std::string imgTail;
		char nResType = reader.readByte(); // 资源类型 1=pvr 2=png 3=jpg 4=pvr.ccz 5=ppm 6=dxt1 7=dxt2 8=dxt3 9=dxt4 10=dxt5 11=tga 12=webp
		switch (nResType)
		{
		case 1:	imgTail = "pvr"; break;
		case 2: imgTail = "png"; break;
		case 3: imgTail = "jpg"; break;
		case 4: imgTail = "pvr.ccz"; break;
		case 5: imgTail = "ppm"; break;
		case 12: imgTail = "webp"; break;
		case 16: return 0; break;
		default: break;
		}
		char nPicCnt = reader.readByte(); // 图片资源数目
		// 读取并加载所有图片资源
		for (int nPicIdx = 0; nPicIdx < nPicCnt; ++nPicIdx)
		{
			int nPicLen = reader.readInt();
			sprintf(szImgPath, "%s%d_%d.%s", szMPImgPath.c_str(), index, nPicIdx, imgTail.c_str());
			reader.write(nPicLen, szImgPath);

		}

		int infolen = 0;
		char nParamNum = reader.readByte();
		infolen ++;
		const unsigned char* pParamStart = reader.readBytes(nParamNum);
		infolen += nParamNum;
		for(int j = 0; j < nParamNum; j++)
		{
			char nParam = pParamStart[j];
			switch (nParam)
			{
			case 0:
				{		
					// 读取mc位置信息
					short nPosX = reader.readShort();
					short nPosY = reader.readShort();
					infolen += 4;
					break;
				}
			case 1:
				{
					float fRotation = reader.readFloat();
					infolen += 4;
					break;
				}
			case 2:
				{
					float fScaleX = reader.readFloat();
					float fScaleY = reader.readFloat();
					infolen += 8;
					break;
				}
			default:
				break;
			}
		}

		// 存储MC信息
		sprintf(szImgPath, "%s_%d.info", szMPImgPath.c_str(), index);
		reader.seek(-infolen);
		reader.write(infolen, szImgPath);
		return nPicCnt;
	}

};

