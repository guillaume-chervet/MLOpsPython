import cuid from 'cuid';
import {loadScripts} from './Script/useScript';

let promiseCache = null;

const convertPdfToImagesAsync = (sources = [`https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.13.216/pdf.min.js`], workerSrc = "") => (file, scale = 2) => {
    if (promiseCache == null) {
        promiseCache = loadScripts(sources).then(() => {
            window.pdfjsLib.GlobalWorkerOptions.workerSrc = workerSrc;
        });
    }
    return promiseCache.then(() => _convertPdfToImagesAsync(window.pdfjsLib, workerSrc, file, scale));
}

const _convertPdfToImagesAsync = (pdfjsLib, workerSrc, file, scale = 2) => {
    return new Promise(resolve => {
        const fileReader = new FileReader();
        fileReader.onload = function (ev) {
            const iDiv = document.createElement('div');
            iDiv.style = 'visibility:hidden;display:none;';
            iDiv.id = cuid();
            document.getElementsByTagName('body')[0].appendChild(iDiv);

            const loadingTask = pdfjsLib.getDocument(fileReader.result);
            return loadingTask.promise.then((pdf) => {
                const numPages = pdf.numPages;
                const tasks = [];
                for (let i = 1; i <= numPages; i++) {
                    const promise = pdf.getPage(i).then(function (page) {
                        const viewport = page.getViewport({scale: scale});
                        const innerDiv = document.createElement('canvas');

                        iDiv.appendChild(innerDiv);

                        const canvas = innerDiv;
                        const context = canvas.getContext('2d');
                        canvas.height = viewport.height;
                        canvas.width = viewport.width;

                        const task = page.render({canvasContext: context, viewport: viewport});
                        return task.promise.then(function () {
                            return canvas.toDataURL('image/png');
                        });
                    });
                    tasks.push(promise);
                }
                return Promise.all(tasks);
            }).then(result => {
                iDiv.remove();
                resolve(result);
            });
        }
        fileReader.readAsArrayBuffer(file);
    });
}


export default convertPdfToImagesAsync;