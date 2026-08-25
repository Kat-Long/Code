(function () {
  const fallback = {
    ja: '本記事は執筆時における現地制度を参考に作成していますが、法令や税制は予告なく変更される場合があります。また、個別具体的な事案における解釈や対応は専門家の意見を必ずご確認ください。本記事の内容を用いたことによるいかなる損害に対しても一切の責任を負いかねます。',
    zh: '本篇文章係參考撰寫當時之當地法規制度所作成，惟法令與稅制可能在未經預告之情況下有所變更。此外，針對個別具體案件之法律解釋與應對方式，請務必諮詢專業人士之意見。對於因使用本篇文章內容而造成之任何損害，本公司概不承擔任何責任。'
  };
  let data = fallback;

  function language() {
    return document.documentElement.lang === 'zh-Hant' || document.documentElement.lang === 'zh' ? 'zh' : 'ja';
  }

  function render() {
    const text = data[language()] || fallback[language()];
    document.querySelectorAll('[data-disclaimer-text]').forEach((element) => {
      element.textContent = text;
    });
  }

  async function load() {
    render();
    try {
      const response = await fetch(new URL('disclaimer.json', document.baseURI), { cache: 'no-store' });
      if (!response.ok) throw new Error('disclaimer.json could not be loaded');
      const json = await response.json();
      if (json && typeof json.ja === 'string' && typeof json.zh === 'string') {
        data = json;
        render();
      }
    } catch (error) {
      console.error('免責事項の読み込みに失敗しました:', error);
      render();
    }
  }

  const start = () => {
    render();
    load();
    new MutationObserver(render).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();
