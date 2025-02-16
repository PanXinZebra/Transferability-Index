
/* Load "Harmonized Sentinel-2 MSI: MultiSpectral Instrument, Level-2A"
// geometry -- a plogon; date1, date2 --- date range;  cloudypercent--- filter cloudy images default value is 20
// clip image and mean collection into a single image*/
exports.pxLoadS2 = function (geometry, date1, date2, cloudypercent) {

    //cloudypercent's default value is 20
    if (cloudypercent === undefined || cloudypercent === null) { var cloudypercent = 20 }
    //this function is google earth engine original clouds mask function
    function maskS2clouds(image) {
        var qa = image.select('QA60');
        // Bits 10 and 11 are clouds and cirrus, respectively.
        var cloudBitMask = 1 << 10;
        var cirrusBitMask = 1 << 11;
        // Both flags should be set to zero, indicating clear conditions.
        var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
            .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
        return image.updateMask(mask).divide(10000);
    }
    //select image which instrect with geometry (will much bigger than geomtry)
    var mycollection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(date1, date2)
        .filterBounds(geometry)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloudypercent))
        .map(maskS2clouds);
    var image = ee.Image(mycollection.mean()).clip(geometry);
    return image;
}

//this function can display Sentinel-2 obtain by pxloadS2
exports.pxDisplayS2 = function (image, imagename) {
    var visualization = {
        min: 0.0,
        max: 0.6,
        bands: ['B4', 'B3', 'B2'],
    };
    Map.addLayer(image, visualization, imagename);
}


/*Load "Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected, log scaling"
//geometry -- a plogon; date1, date2 --- date range;
//bandname --- is in 'VV' or 'VH'
//clip image and mean collection into a single image*/
exports.pxLoadS1 = function (geometry, date1, date2, bandname) {

    var mycollection = ee.ImageCollection('COPERNICUS/S1_GRD')
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', bandname))
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .select(bandname);

    var image = mycollection.filterDate(date1, date2)
        .filterBounds(geometry);
    var realimage = ee.Image(image.mean()).clip(geometry);
    return realimage;
}


//this function can display Sentinel-1 obtain by pxloadS1
exports.pxDisplayS1 = function (image, imagename) {
    Map.addLayer(image, { min: -25, max: 5 }, imagename, true);
}

//Perform snic segmentation on S2 image
exports.pxImageClusterOnS2SNIC = function (image) {
    var seeds = ee.Algorithms.Image.Segmentation.seedGrid(25);
    var snic = ee.Algorithms.Image.Segmentation.SNIC({
        image: image,
        size: 25,
        compactness: 3,
        connectivity: 8,
        neighborhoodSize: 20,
        seeds: seeds
    });
    return (snic);
}

//Perform GMeans segmentation on S2 image
exports.pxImageClusterOnS2GMeans = function (image) {
    var gmeans = ee.Algorithms.Image.Segmentation.GMeans({
        image: image,
        neighborhoodSize: 20
    });
    return gmeans;
}

exports.pxImageClusterOnS2KMeans = function (image) {
    var gmeans = ee.Algorithms.Image.Segmentation.KMeans({
        image: image,
    });
    return gmeans;
}

//this function can display cluster result from pxImageClusterOnS2
exports.pxDisplayClustersFromS2 = function (image, imagename) {
    var clusters = image.select('clusters')
    Map.addLayer(clusters.randomVisualizer(), {}, imagename)
}

//reduce S1 single band image with cluster result,
exports.pxReduceClusterOnS1 = function (image, clusterimage) {
    var clusimage = clusterimage.select("clusters");
    var rr = image.addBands(clusimage);
    var reducmean = rr.reduceConnectedComponents(ee.Reducer.mean(), 'clusters');
    return reducmean;
}

//this function can display reduce cluster on s1
exports.pxDisplayReduceClusterS1 = function (image, imagename) {
    Map.addLayer(image, { min: -25, max: 5 }, imagename, true);
}