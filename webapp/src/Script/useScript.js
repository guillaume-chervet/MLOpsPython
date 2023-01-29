import {useEffect, useState} from 'react';

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const cachedScripts = [];
const loadingScripts = [];
const useScript = (src) => {
    // Keeping track of script loaded and error state
    const [state, setState] = useState({
        loaded: false,
        error: false,
    });

    useEffect(
        () => {
            const loadScript = () => {
                // If cachedScripts array already includes src that means another instance ...
                // ... of this hook already loaded this script, so no need to load again.
                if (loadingScripts.includes(src)) {
                    const promise = sleep(50);
                    promise.then(loadScript);
                    return {state: 'waiting', promise};
                }
                if (cachedScripts.includes(src)) {
                    setState({
                        loaded: true,
                        error: false,
                    });
                    return {state: 'loaded'};
                }
                loadingScripts.push(src);
                // Create script
                const script = document.createElement('script');
                script.src = src;
                script.async = true;

                const removeLoadingScript = () => {
                    // Remove from cachedScripts we can try loading again
                    const index = loadingScripts.indexOf(src);
                    if (index >= 0) loadingScripts.splice(index, 1);
                };

                // Script event listener callbacks for load and error
                const onScriptLoad = () => {
                    removeLoadingScript();
                    cachedScripts.push(src);
                    setState({
                        loaded: true,
                        error: false,
                    });
                };

                const onScriptError = () => {
                    removeLoadingScript();
                    script.remove();
                    setState({
                        loaded: true,
                        error: true,
                    });
                };

                script.addEventListener('load', onScriptLoad);
                script.addEventListener('error', onScriptError);

                // Add script to document body
                document.body.appendChild(script);

                // Remove event listeners on cleanup
                return {
                    state: 'loading',
                    callbacks: () => {
                        script.removeEventListener('load', onScriptLoad);
                        script.removeEventListener('error', onScriptError);
                    },
                };
            };

            const result = loadScript();
            if (result.state === 'loading') {
                return result.callbacks;
            }
        },
        [src], // Only re-run effect if script src changes
    );

    return [state.loaded, state.error];
};

export const loadScripts = (sources) => {
    const promises = sources.map(loadScript);
    return Promise.all(promises);
}

export const loadScript = (src) => {
    // If cachedScripts array already includes src that means another instance ...
    // ... of this hook already loaded this script, so no need to load again.
    if (loadingScripts.includes(src)) {
        const promise = sleep(50);
        return promise.then(() => loadScript(src));
    }
    if (cachedScripts.includes(src)) {
        return new Promise(resolve => resolve());
    }
    loadingScripts.push(src);
    // Create script
    const script = document.createElement('script');
    script.src = src;
    script.async = true;

    const removeLoadingScript = () => {
        // Remove from cachedScripts we can try loading again
        const index = loadingScripts.indexOf(src);
        if (index >= 0) loadingScripts.splice(index, 1);
    };

    return new Promise((resolve, error) => {
        // Script event listener callbacks for load and error
        const onScriptLoad = () => {
            cachedScripts.push(src);
            removeLoadingScript();
            resolve();
        };

        const onScriptError = () => {
            script.remove();
            removeLoadingScript();
            error();
        };

        script.addEventListener('load', onScriptLoad);
        script.addEventListener('error', onScriptError);

        // Add script to document body
        document.body.appendChild(script);
    });
};


export default useScript;