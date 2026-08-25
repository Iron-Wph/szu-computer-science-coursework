self.onmessage = function (e) {
    const { start, end } = e.data;
    let count = 0;
    for (let num = start; num <= end; num++) {
        if (isPrime(num)) {
            count++;
        }
        if (count % 1000 === 0 && count !== 0) {
            // 返回质数数量
            self.postMessage({ type: 'progress', count: count });
        }
    }
    // 返回最终的质数数量
    self.postMessage({ type: 'result', count: count });
}

// TODO 检查一个数是否为质数 (可优化，最终均需要放到worker.js中)
function isPrime(num) {
    // 小于1返回false
    if (num <= 1) return false;
    // 2和3都是质数
    if (num <= 3) return true;
    // 是2或3的倍数
    if (num % 2 === 0 || num % 3 === 0)
        return false;

    // 不是6的倍数
    for (let i = 5; i <= Math.sqrt(num); i += 6) {
        if (num % i === 0 || num % (i + 2) === 0)
            return false;
    }
    return true;
}