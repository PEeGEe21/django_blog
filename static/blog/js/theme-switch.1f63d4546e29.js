(function() {
    // Theme switch
    var themeSwitch = document.getElementById('themeSwitchToggle');
    if(themeSwitch) {
      initTheme(); // if user has already selected a specific theme -> apply it
      themeSwitch.addEventListener('change', function(event){
        resetTheme(); // update color theme
      });
  
      function initTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
          document.documentElement.classList.add('theme-dark');
          window.localStorage.setItem('themeSwitch','dark');
        }   
        var darkThemeSelected = (localStorage.getItem('themeSwitch') !== null && localStorage.getItem('themeSwitch') === 'dark');
        // update checkbox
        themeSwitch.checked = darkThemeSelected;
        // update class on html element
        darkThemeSelected ? document.documentElement.classList.add('theme-dark') : document.documentElement.classList.remove('theme-dark');
      };
  
      function resetTheme() {
        if(themeSwitch.checked) { // dark theme has been selected
          document.documentElement.classList.add('theme-dark');
          localStorage.setItem('themeSwitch', 'dark');
        } else {
          document.documentElement.classList.remove('theme-dark');
          localStorage.removeItem('themeSwitch');
        }
      };
    }
  }());