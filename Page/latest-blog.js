(function () {
    const fixedIds = [6, 2];

    function getLanguage() {
        const htmlLanguage = document.documentElement.lang;
        if (htmlLanguage === 'zh' || htmlLanguage === 'zh-Hant') return 'zh';
        const button = document.querySelector('.lang-switch, .lang, #lang-button, #language-button');
        return button && button.textContent.trim() === '日本語' ? 'zh' : 'ja';
    }

    function getLatestArticles(articles) {
        const byId = new Map(articles.map(article => [Number(article.id), article]));
        const fixed = fixedIds.map(id => byId.get(id)).filter(Boolean);
        const remaining = articles
            .filter(article => !fixedIds.includes(Number(article.id)))
            .sort((a, b) => new Date(b.date) - new Date(a.date));
        return [...fixed, ...remaining].slice(0, 3);
    }

    function renderLatestBlogs(articles) {
        const language = getLanguage();
        const titleKey = language === 'ja' ? 'title_ja' : 'title_zh';
        const excerptKey = language === 'ja' ? 'excerpt_ja' : 'excerpt_zh';
        const linkKey = `external_link_${language}`;
        const readMore = language === 'ja' ? '続きを読む →' : '繼續閱讀 →';

        document.querySelectorAll('.latest-blog-grid').forEach(grid => {
            grid.innerHTML = getLatestArticles(articles).map(article => {
                const destination = article[linkKey] || 'blog.html';
                return `<article class="latest-blog-card" data-link="${destination}" tabindex="0">
                    <img src="${article.image}" alt="${article[titleKey]}" loading="lazy">
                    <div class="latest-blog-card-header"><h3>${article[titleKey]}</h3><div class="latest-blog-date">${article.date}</div></div>
                    <div class="latest-blog-card-body"><p>${article[excerptKey]}</p><a class="latest-blog-read-more" href="${destination}">${readMore}</a></div>
                </article>`;
            }).join('');
            grid.querySelectorAll('.latest-blog-card').forEach(card => {
                const go = event => {
                    if (event && event.target.closest('a')) return;
                    window.location.href = card.dataset.link;
                };
                card.addEventListener('click', go);
                card.addEventListener('keydown', event => {
                    if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); go(event); }
                });
            });
        });
    }

    async function loadLatestBlogs() {
        try {
            const response = await fetch('articles.json', { cache: 'no-store' });
            if (!response.ok) throw new Error('記事データの取得に失敗しました。');
            const data = await response.json();
            window.latestBlogArticles = data.articles || [];
            renderLatestBlogs(window.latestBlogArticles);
        } catch (error) {
            console.error('Error loading latest blogs:', error);
        }
    }

    window.renderLatestBlogs = () => {
        if (window.latestBlogArticles) renderLatestBlogs(window.latestBlogArticles);
    };
    document.addEventListener('DOMContentLoaded', loadLatestBlogs);
    document.addEventListener('click', event => {
        if (event.target.closest('.lang-switch, .lang, #lang-button, #language-button')) {
            setTimeout(window.renderLatestBlogs, 0);
        }
    });
})();