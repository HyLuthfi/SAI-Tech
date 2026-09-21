/**
 * SAI Tech Enterprise - Global Motion & Kinetic Engine
 * Real-time 3D card physics, smooth counter animation,
 * and portfolio drag scroll. Scroll entrance animations are
 * handled natively by Webflow IX2 runtime (slideInBottom).
 */
(function () {
  'use strict';

  // 0. Clean URL Engine: Immediately strip .html from browser address bar
  if (typeof window !== 'undefined' && window.location && window.location.pathname) {
    var pathname = window.location.pathname;
    if (pathname.endsWith('.html')) {
      var clean = pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
      if (!clean) clean = '/';
      window.history.replaceState(null, '', clean + window.location.search + window.location.hash);
    }
  }

  function initMotion() {
    // 1. Real-Time 3D Tilt & Cursor Spotlight on Enterprise Cards
    var interactiveCards = document.querySelectorAll(
      '.portfolio-card, .services-single, .pricing-single-card, .team-member-wrapper, .blog-single, .about-us-card'
    );

    interactiveCards.forEach(function (card) {
      var isHovered = false;
      var rafId = null;

      card.addEventListener('mouseenter', function () {
        isHovered = true;
      });

      card.addEventListener('mousemove', function (e) {
        if (!isHovered) return;
        var rect = card.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;

        if (rafId) cancelAnimationFrame(rafId);
        rafId = requestAnimationFrame(function () {
          card.style.setProperty('--mouse-x', x + 'px');
          card.style.setProperty('--mouse-y', y + 'px');

          var centerX = rect.width / 2;
          var centerY = rect.height / 2;
          var rotateX = (((y - centerY) / centerY) * -4).toFixed(2);
          var rotateY = (((x - centerX) / centerX) * 4).toFixed(2);

          card.style.transform =
            'perspective(1000px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) translateY(-6px)';
        });
      });

      card.addEventListener('mouseleave', function () {
        isHovered = false;
        if (rafId) cancelAnimationFrame(rafId);
        card.style.transform = '';
      });
    });

    // 2. Smooth Counter Animation for Metrics (General Pages)
    var counterElements = document.querySelectorAll('.counter-number, .stat-value, .about-us-card-number');
    if (counterElements.length) {
      var counterObserver = new IntersectionObserver(
        function (entries, observer) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              var target = entry.target;
              var text = target.innerText.trim();
              var match = text.match(/([0-9.,]+)/);
              if (match) {
                var rawNum = parseFloat(match[1].replace(/,/g, ''));
                var prefix = text.slice(0, match.index);
                var suffix = text.slice(match.index + match[1].length);
                var duration = 1600;
                var startTime = performance.now();

                function updateCounter(currentTime) {
                  var elapsed = currentTime - startTime;
                  var progress = Math.min(elapsed / duration, 1);
                  var easeOut = 1 - Math.pow(1 - progress, 3);
                  var currentVal = (rawNum * easeOut).toFixed(text.includes('.') ? 1 : 0);
                  target.innerText = prefix + currentVal + suffix;

                  if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                  } else {
                    target.innerText = text;
                  }
                }
                requestAnimationFrame(updateCounter);
              }
              observer.unobserve(target);
            }
          });
        },
        { threshold: 0.2 }
      );

      counterElements.forEach(function (el) {
        counterObserver.observe(el);
      });
    }

    // 3. Portfolio Horizontal Drag Scroll & Touch Inertia
    var tickerWrapper = document.querySelector('.portfolio-ticker');
    if (tickerWrapper) {
      var isDown = false;
      var startX;
      var scrollLeft;

      tickerWrapper.addEventListener('mousedown', function (e) {
        isDown = true;
        tickerWrapper.style.cursor = 'grabbing';
        startX = e.pageX - tickerWrapper.offsetLeft;
        scrollLeft = tickerWrapper.scrollLeft;
      });

      tickerWrapper.addEventListener('mouseleave', function () {
        isDown = false;
        tickerWrapper.style.cursor = '';
      });

      tickerWrapper.addEventListener('mouseup', function () {
        isDown = false;
        tickerWrapper.style.cursor = '';
      });

      tickerWrapper.addEventListener('mousemove', function (e) {
        if (!isDown) return;
        e.preventDefault();
        var x = e.pageX - tickerWrapper.offsetLeft;
        var walk = (x - startX) * 1.5;
        tickerWrapper.scrollLeft = scrollLeft - walk;
      });
    }

    // 4. Universal Enterprise Newsletter Submission Handler
    document.addEventListener('submit', function (e) {
      var form = e.target;
      if (form && (form.id === 'wf-form-Newsletter-Form' || form.getAttribute('data-name') === 'Newsletter Form')) {
        e.preventDefault();
        e.stopPropagation();

        var input = form.querySelector('input[type="email"]');
        var email = (input ? input.value : '').trim();
        if (!email) return;

        try {
          var subscribers = JSON.parse(localStorage.getItem('sai_newsletter_subscribers') || '[]');
          subscribers.unshift({
            email: email,
            subscribedAt: new Date().toISOString()
          });
          localStorage.setItem('sai_newsletter_subscribers', JSON.stringify(subscribers));
        } catch (err) {}

        var container = form.closest('.footer-form-block') || form.parentElement;
        var doneBox = container.querySelector('.w-form-done');
        var failBox = container.querySelector('.w-form-fail');

        if (failBox) failBox.style.display = 'none';

        if (doneBox) {
          form.style.display = 'none';
          doneBox.style.display = 'block';
          doneBox.innerHTML =
            '<div style="text-align: left; padding: 16px 20px; background: rgba(0, 0, 77, 0.4); border: 1px solid rgba(230, 194, 106, 0.4); border-radius: 14px;">' +
            '<div style="color: #22c55e; font-weight: 700; margin-bottom: 4px; display: flex; align-items: center; gap: 8px;">✓ Pendaftaran Berhasil!</div>' +
            '<div style="color: rgba(246, 246, 249, 0.9); font-size: 13.5px; line-height: 1.5;">' +
            'Email <strong>' +
            email.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') +
            '</strong> telah terdaftar. Kami akan mengirimkan ringkasan riset arsitektur AI dan benchmark GPU secara berkala.' +
            '</div>' +
            '</div>';
        }
      }
    });
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMotion);
  } else {
    initMotion();
  }
})();
