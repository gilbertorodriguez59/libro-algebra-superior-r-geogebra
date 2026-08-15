(function (global) {
  "use strict";

  function formatNumber(value, digits) {
    if (!Number.isFinite(Number(value))) return "—";
    return Number(value).toLocaleString("es-MX", {
      maximumFractionDigits: digits,
      minimumFractionDigits: 0
    });
  }

  function showLoadError(message) {
    var box = document.querySelector(".error");
    if (box) {
      box.hidden = false;
      box.textContent = message || box.textContent;
    }
    var status = document.getElementById("status");
    if (status) status.textContent = "GeoGebra no pudo cargarse.";
  }

  function params(onLoad) {
    return {
      appName: "graphing",
      width: 1100,
      height: 620,
      showToolBar: true,
      showAlgebraInput: true,
      showMenuBar: false,
      enableShiftDragZoom: true,
      language: "es",
      scaleContainerClass: "ggb-container",
      autoHeight: true,
      appletOnLoad: function (api) {
        var error = document.querySelector(".error");
        if (error) error.hidden = true;
        try {
          onLoad(api);
        } catch (err) {
          showLoadError("La construcción se cargó, pero no pudo inicializarse: " + err.message);
          throw err;
        }
      }
    };
  }

  function inject(appletParams) {
    if (typeof global.GGBApplet !== "function") {
      showLoadError("No fue posible descargar el componente de GeoGebra. Compruebe la conexión a Internet o descargue el archivo .ggb base.");
      return;
    }
    try {
      var applet = new global.GGBApplet(appletParams, true);
      applet.inject("ggb-element");
    } catch (err) {
      showLoadError("No fue posible iniciar GeoGebra: " + err.message);
    }
  }

  function configure(api, xmin, xmax, ymin, ymax) {
    api.setCoordSystem(xmin, xmax, ymin, ymax);
    try { api.setAxesVisible(true, true); } catch (err) { /* API antigua */ }
    try { api.setGridVisible(true); } catch (err) { /* API antigua */ }
  }

  function style(api, name, color, thickness) {
    api.setColor(name, color[0], color[1], color[2]);
    if (thickness) {
      try { api.setLineThickness(name, thickness); } catch (err) { /* objeto sin línea */ }
    }
  }

  function fit(api) {
    try { api.setMode(0); } catch (err) { /* API antigua */ }
  }

  function saveBase64(base64, filename) {
    var binary = global.atob(base64);
    var bytes = new Uint8Array(binary.length);
    for (var i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
    var blob = new Blob([bytes], { type: "application/vnd.geogebra.file" });
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    global.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function download(api, filename) {
    if (!api || typeof api.getBase64 !== "function") {
      showLoadError("GeoGebra aún no está listo para exportar la construcción.");
      return;
    }
    var completed = false;
    var callback = function (base64) {
      if (!completed && base64) {
        completed = true;
        saveBase64(base64, filename);
      }
    };
    try {
      var returned = api.getBase64(callback);
      if (typeof returned === "string") callback(returned);
    } catch (err) {
      showLoadError("No fue posible exportar la construcción: " + err.message);
    }
  }

  global.GGBLab = {
    fmt: formatNumber,
    params: params,
    inject: inject,
    configure: configure,
    style: style,
    fit: fit,
    download: download
  };
}(window));
