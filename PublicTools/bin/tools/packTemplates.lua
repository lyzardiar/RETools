local args = { ... }

--[[
local t={
	[1001]={
		["ID"] = 1001,
		["Description"] = "燃烧",
	},
	[1004]={
		["ID"] = 1004,
		["Description"] = "好不容易控制住了列车，啵咕空贼团又追了上来。",
	},
}
]]
function work(filepath)
    print("pack:", filepath)
    local keys = {}

    local file = io.open(filepath, "rb")
    local str = file:read("*all")
    file:close()
    
    if str:find("setmetatable") then return end
    
    local isParse = false
    string.gsub(str, "t=%{.-%[%d-%]=%{(.-)%}%,%s", function(val)
        if not isParse then 
            isParse = true
            
            string.gsub(val, '%[(%b"")%]', function(key)                
                keys[#keys + 1] = string.sub(key, 2, #key - 1)
            end)
            
        end
    end)

    local ret, stat = dofile(filepath)
 
    local indexs = {}
    local indexContents = "local indexs = { "
    for k, v in pairs(keys) do 
        indexs[v] = k
        indexContents = indexContents .. string.format([[ ["%s"] = %d, ]], v, k)
    end
    indexContents = indexContents .. ' }'
    
    local content = string.format([[
%s
local mt = {  
    __index = function(t, key)
        local index = indexs[key]
        if index then 
            return t[index]
        end
    end
}

local t = {]], indexContents)
    
    for k, v in pairs(ret) do 
        local line = string.format("[%d] = { ", v[keys[1]])
        for _, key in ipairs(keys) do 
            local val = v[key]
            local tp = type(val)
            if tp == 'string' then 
                line = string.format("%s\"%s\", ", line, val)
            elseif tp == 'bool' then 
                line = string.format("%s%s, ", line, val and "true" or "false")
            elseif tp == 'number' then 
                line = string.format("%s%d, ", line, val)
            end
        end
        line = line .. '},'
        
        content = string.format('%s\n\t%s', content, line)
    end
    
    content = content .. '\n}\nsetmetatable(t, mt)\nreturn t'
 
    local file = io.open(filepath .. '', "wb")
    file:write(content)
    file:close()   
end

for k, v in ipairs(args) do 
    work(v)
end