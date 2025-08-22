import { useEffect } from 'react';

export default function LiquidNavbar() {
  useEffect(() => {
    let ticking = false;
    
    function updateNavbar() {
      const navbar = document.querySelector('.navbar');
      if (!navbar) return;
      
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      if (scrollTop > 50) {
        navbar.classList.add('navbar--scrolled');
      } else {
        navbar.classList.remove('navbar--scrolled');
      }
      
      ticking = false;
    }
    
    function requestTick() {
      if (!ticking) {
        requestAnimationFrame(updateNavbar);
        ticking = true;
      }
    }
    
    // 初始检查
    updateNavbar();
    
    // 添加滚动监听器
    window.addEventListener('scroll', requestTick, { passive: true });
    
    // 添加鼠标移动效果
    const navbar = document.querySelector('.navbar');
    if (navbar) {
      navbar.addEventListener('mousemove', (e) => {
        const rect = navbar.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        
        navbar.style.setProperty('--mouse-x', `${x}%`);
      });
    }
    
    return () => {
      window.removeEventListener('scroll', requestTick);
    };
  }, []);
  
  return null;
}
