// Operator to do addtion or subtraction
function operateHexColors(c1, c2, accumulator) {
      var hexStr 
      if (typeof(c2) ==='string') {
         hexStr = accumulator(parseInt(c1, 16), parseInt(c2, 16)).toString(16)  
      } else {
         hexStr = (parseInt(c1, 16) * c2).toString(16)  
      }
      while (hexStr.len) {
          hexStr = '0' + hexStr;
      }
      return hexStr
}

let divergingScheme = ["#93003a", "#ae1045", "#c52a52", "#d84360", "#e75d6f", "#f4777f", "#fd9291", "#ffaea5", "#ffcab9", "#ffe5cc", "#efec6b", "#deda5a", "#cac94b", "#b4b93e", "#9da932", "#849a26", "#6b8c1c", "#507e11", "#326f07", "#006100"]


export function getColorGradient(key) {
    const shift = (key + 1)
    return divergingScheme[Math.round(shift * 10)]
}


export function extrapolateGradient(c1, c2, key) {

    const subtract = (a, b) => {return b - a}
    const add = (a, b) => {return a + b}
    const multiply = (a, b) => {return a * b}
    const diff = operateHexColors(c1, c2, subtract)
 
    return operateHexColors(c1, operateHexColors(diff, key ,multiply), add)

}
