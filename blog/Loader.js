window.QMM = window.QMM || {};
(function (global) {
    var DOC = window.document;
    var HEAD = document.getElementsByTagName("head")[0];
    var reg_readystate = /loaded|complete|undefined/i;
    var method = DOC.dispatchEvent ? "onload" : "onreadystatechange";
    var counter = 1; //get计数器
    var ifmCt = 1; //post计数器
    var isOpera = navigator.userAgent.toLowerCase().indexOf("opera") >= 0;
    var arrTokens = [];
    var nothing = function(){return false};

    var pForm = document.getElementById("ifrmSender");
    var pFrame = document.getElementById("ifrmLoader");
    var hiddenInputs = []; //post参数


    //全局回调函数命名空间
    var MyLoader = {};

    //获取随机回调函数名
    function getCb() {
        return "cb" + new Date().getTime().toString(36) + (counter++).toString(36);
    }
    //获取字符串字节长度
    function getByteLength(str) {
        return str.replace(/[^\x00-\xff]/g, "--").length;
    }

    //删除script标签
    function removeScript(node) {
        if (typeof node === "string") {
            node = DOC.getElementById(node);
        }
        if (!node || node.tagName !== "SCRIPT") {
            return;
        }
        if (node.clearAttributes) {
            node.clearAttributes();
        }
        node[method] = node.onerror = null;
        if (node.parentNode) {
            node.parentNode.removeChild(node);
        }
    }
    //兼容opera浏览器script标签的onerror事件
    function fixOperaError(name, url, onerror) {
        var code = '<script src="' + url + '" ' + method + '="this.ownerDocument.z = 1"></script>';
        var iframe = DOC.createElement("iframe");
        iframe.style.display = "none";
        HEAD.appendChild(iframe);
        var ifrDoc = iframe.contentDocument;
        iframe.onload = function () {
            if (ifrDoc.z != 1) {
                removeScript(name);
                onerror && onerror();
            }
            iframe.onload = null; //opera无法在iframe被事件绑定时被移除
            HEAD.removeChild(this);
        };
        try {
            ifrDoc.write(code);
            ifrDoc.close();
        } catch (ex) { }
    }

    function setFormParams(form, arrParams) {
        var len = Math.max(arrParams.length, hiddenInputs.length);
        for (var i = 0, param, hiddenInput, j; i < len; i++) {
            param = arrParams[i];
            hiddenInput = hiddenInputs[i];
            if (param) {
                j = param.indexOf("=");
                if (!hiddenInput) {
                    hiddenInput = hiddenInputs[i] = DOC.createElement("input");
                    hiddenInput.type = "text";
                }
                hiddenInput.name = param.substring(0, j);
                hiddenInput.value = decodeURIComponent(param.substring(j + 1));
                form.appendChild(hiddenInput);
            } else if (hiddenInput && hiddenInput.parentNode) {
                hiddenInput.parentNode.removeChild(hiddenInput);
                hiddenInput.name = "";
                hiddenInput.value = "";
            }
        }
    }

    function getXHR() {
        if (window.ActiveXObject) {
            try {
                return new ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
                try {
                    return new ActiveXObject("Microsoft.XMLHTTP");
                } catch (e) { }
            }
        }
        if (window.XMLHttpRequest) {
            return new XMLHttpRequest();
        }
        return null;
    }

    function saveToken(name, type, sender) {
        arrTokens.push({
            name: name,
            type: type,
            sender: sender
        });
    }

    var searchTimer = null;
    function showSearching() {
        if (searchTimer) {
            clearTimeout(searchTimer);
            searchTimer = null;
        } else {
            $('Searching').innerHTML = QMM.RC.Searching +
                '&nbsp;<img src="' + QMM.Config.getImageUrl('searching.gif') +
                '"></img>';
            $('Searching').style.display = '';
        }
    }

    function hideSearching() {
        if (searchTimer) {
            clearTimeout(searchTimer);
            searchTimer = null;
        } else {
            searchTimer = setTimeout(function() {
                $('Searching').style.display = 'none';
                searchTimer = null;
            }, 200);
        }
    }

    var Sender = {
        script: function (name, url, onload, onerror, status, charset) {//jsonp
            var node = DOC.createElement("script");
            saveToken(name, 0, node);
            node.setAttribute('type', 'text/javascript');
            node.setAttribute('charset', charset || 'gbk');
            node.async = true;
            node.id = name;
            var result = null;
            node[method] = function () {
                if (reg_readystate.test(this.readyState)) {
                    if (result) {
                        onload && onload(result);
                    } else {
                        onerror && onerror();
                    }
                    //hideSearching();
                    Loader.destroy(name);
                }
            };
            MyLoader[name] = function (jsonObj) {
                result = jsonObj;
            };
            node.onerror = function () {
                onerror && onerror();
                Loader.destroy(name);
                //hideSearching();
            };
            var f = [
                "output=jsonp",
                "cb=MyLoader." + name
            ];
            var src =
                url + (url.indexOf("?") === -1 ? "?" : "&") + f.join("&");
            node.src = src;
            HEAD.insertBefore(node, HEAD.firstChild);
        },
        frame: function (name, url, onload, onerror,state) {
            var method = getByteLength(url) < 2048 ? "get" : "post";
            var q = url.indexOf("?");
            var action = q < 0 ? postEngine : url.substring(0, q);
            var host = window.location.host;
            if(!host || action.indexOf(host)===-1){
                Sender.script.apply(null,arguments);
                return;
            }
            var params = url.substring(q + 1).split("&");
            params.push("output=html");
            params.push("cb=parent.MyLoader." + name);
            if(state){
                params.push("state="+state);
            }
            setFormParams(pForm, params);
            pForm.method = method;
            pForm.action = action;

            saveToken(name, 1, pFrame);

            MyLoader[name] = function (result,state) {
                result = QMM.Util.clone(result);
                onload && onload(result,state);
                //hideSearching();
            };
            if(MyImpl.Util.Browser().chrome){
                var src = action + "?"+ params.join("&");
                if(console){
                    console.log("frameSrc:"+src);
                }
                pFrame.src = src;
            }else{
                pForm.submit();
            }
        },
        xhr: function (name, url, onload, onerror) {//post
            var method = getByteLength(url) < 2048 ? "get" : "post";
            var xhr = getXHR();
            xhr.open(method, url, true);
            xhr.onreadystatechange=function(){
                if (xhr.readyState == 4) {
                    try {
                        var stat = xhr.status;
                    } catch (ex) {
                        onerror && onerror();
                        //hideSearching();
                        return;
                    }
                    if (stat === 200) {
                        onload && onload(eval(xhr.responseText));
                        //hideSearching();
                    } else {
                        onerror && onerror();
                        //hideSearching();
                    }
                   /* window.setTimeout(
                        function() {
                            xhr.onreadystatechange = nothing;
                            xhr = null;
                        }, 0);*/
                }
            };
            xhr.send(null);
        }
    };

    var Loader = {
        send: function (name, url, onload, onerror, options) {
            Loader.destroy(name);
            name = !name ? getCb() : name;
            options = options || {};
            url = (url.indexOf('http://') == -1 ? QMMDomain : '') + url;
            var args = [].slice.call(arguments, 0, 4);
            if(options.state){
                args[4] = options.state;
            }
            if (options.charset) {
                args[5] = options.charset;
            }
            if (options.isHistory) {
                Sender.frame.apply(null, args);
            } else {
                if (getByteLength(url) >= 2048) {
                    Sender.xhr.apply(null, args);
                } else {
                    Sender.script.apply(null, args);
                }
            }
            return name;
        },

        loadJs: function (src, callback, charset) {
            var node = DOC.createElement("script");
            node.setAttribute('type', 'text/javascript');
            if (charset) {
                node.setAttribute('charset', charset);
            }
            node.async = true;
            node[method] = function () {
                if (reg_readystate.test(this.readyState)) {
                    callback && callback();
                    removeScript(this);
                }
            };
            node.onerror = function () {
                callback && callback();
                removeScript(this);
            };
            node.src = (src.indexOf('http://') == -1 ? QMMDomain : '') + src;
            isOpera && fixOperaError(name, url, onerror);
            HEAD.insertBefore(node, HEAD.firstChild);
        },
        destroy: function (tokenName) {
            var i = 0,
                len = arrTokens,
                tokenObj = null;
            for (; i < len; i++) {
                if (arrTokens[i].name === tokenName) {
                    tokenObj = arrTokens.splice(i, 1);
                }
            }
            if (tokenObj) {
                switch (tokenObj.type) {
                    case 0:
                        removeScript(tokenObj.sender);
                        break;
                    case 1:
                        stopFrame(tokenObj.sender);
                        break;
                    case 2:
                        break;
                }
            }
            if (MyLoader[tokenName]&&(!tokenObj||tokenObj.type!==1)) {
                delete MyLoader[tokenName];
            }
        }
    };

    global["Loader"] = Loader;
    window["MyLoader"] = MyLoader;
})(window);