/**
 * Created by weijing on 2018/4/13.
 */
function sotitle(id, arr) {
    var title;


    $.each(arr, function (index, obj) {
        if(obj.id==id){
            title = obj.name;
        }

    });

    if (title == null) {
        return '';
    } else {
        return title;
    }

}
//时间戳的处理
function toDateString(d, format){
    var date = new Date(d || new Date())
        ,ymd = [
        digit(date.getFullYear(), 4)
        ,digit(date.getMonth() + 1)
        ,digit(date.getDate())
    ]
        ,hms = [
        digit(date.getHours())
        ,digit(date.getMinutes())
        ,digit(date.getSeconds())
    ];

    format = format || 'yyyy-MM-dd HH:mm:ss';

    return format.replace(/yyyy/g, ymd[0])
        .replace(/MM/g, ymd[1])
        .replace(/dd/g, ymd[2])
        .replace(/HH/g, hms[0])
        .replace(/mm/g, hms[1])
        .replace(/ss/g, hms[2]);
}

//数字前置补零
function digit(num, length, end){
    var str = '';
    num = String(num);
    length = length || 2;
    for(var i = num.length; i < length; i++){
        str += '0';
    }
    return num < Math.pow(10, length) ? str + (num|0) : num;
}


function str16ToBit (str) {
      let result = '';
      // 转字符串
      str += '';
      for (let i = 0; i < str.length; i++) {
        let bit = parseInt(str[i], 16).toString(2);
        // 转字符串
        bit.toString();
        // 补零
        while (bit.length < 4) {
          bit = '0' + bit;
        }
        result += bit;
      }
      return result
}
