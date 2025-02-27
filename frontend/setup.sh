#!/bin/bash

# 安装前端依赖
echo "正在安装前端依赖..."
npm install

# 检查是否安装了 react-router-dom
if npm list react-router-dom > /dev/null 2>&1; then
    echo "react-router-dom 已安装"
else
    echo "正在安装 react-router-dom..."
    npm install react-router-dom
fi

# 检查是否安装了 socket.io-client
if npm list socket.io-client > /dev/null 2>&1; then
    echo "socket.io-client 已安装"
else
    echo "正在安装 socket.io-client..."
    npm install socket.io-client
fi

# 检查是否安装了 react-dropzone
if npm list react-dropzone > /dev/null 2>&1; then
    echo "react-dropzone 已安装"
else
    echo "正在安装 react-dropzone..."
    npm install react-dropzone
fi

# 检查是否安装了 postcss-preset-env
if npm list postcss-preset-env > /dev/null 2>&1; then
    echo "postcss-preset-env 已安装"
else
    echo "正在安装 postcss-preset-env..."
    npm install postcss-preset-env --save-dev
fi

# 检查是否安装了 @tailwindcss/forms
if npm list @tailwindcss/forms > /dev/null 2>&1; then
    echo "@tailwindcss/forms 已安装"
else
    echo "正在安装 @tailwindcss/forms..."
    npm install @tailwindcss/forms
fi

echo "前端依赖安装完成!" 