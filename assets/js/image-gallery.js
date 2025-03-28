document.addEventListener('DOMContentLoaded', function() {
    // 创建图片查看器
    const viewer = document.createElement('div');
    viewer.className = 'image-viewer';
    const viewerImg = document.createElement('img');
    const closeBtn = document.createElement('span');
    closeBtn.className = 'close';
    closeBtn.innerHTML = '×';
    viewer.appendChild(viewerImg);
    viewer.appendChild(closeBtn);
    document.body.appendChild(viewer);

    // 处理图片点击
    const galleryImages = document.querySelectorAll('.image-example img');
    galleryImages.forEach(img => {
        // 添加加载状态
        img.classList.add('loading');
        img.onload = () => {
            img.classList.remove('loading');
        };

        // 点击放大查看
        img.addEventListener('click', function() {
            viewerImg.src = this.src;
            viewer.classList.add('active');
        });
    });

    // 关闭查看器
    closeBtn.addEventListener('click', () => {
        viewer.classList.remove('active');
    });

    // 点击背景关闭
    viewer.addEventListener('click', (e) => {
        if (e.target === viewer) {
            viewer.classList.remove('active');
        }
    });

    // ESC键关闭
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && viewer.classList.contains('active')) {
            viewer.classList.remove('active');
        }
    });

    // 图片错误处理
    const handleImageError = (img) => {
        img.src = '/assets/images/placeholder.png'; // 设置默认占位图
        img.classList.remove('loading');
        img.classList.add('error');
    };

    galleryImages.forEach(img => {
        img.onerror = () => handleImageError(img);
    });

    // 懒加载图片
    const lazyLoadImages = () => {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    };

    // 如果浏览器支持，启用懒加载
    if ('IntersectionObserver' in window) {
        lazyLoadImages();
    }

    // 风格卡片悬停效果
    const styleCards = document.querySelectorAll('.style-card');
    styleCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
}); 