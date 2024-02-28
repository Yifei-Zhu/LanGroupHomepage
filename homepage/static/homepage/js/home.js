window.addEventListener('scroll', function() {
    var scrollPosition = window.pageYOffset; // 获取垂直滚动位置
    var opacity = 1 - (scrollPosition / 2000); // 计算不透明度
    document.querySelector('.header-image').style.opacity = opacity > 0.2 ? opacity : 0.2;
});

