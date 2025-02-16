var table = ee.FeatureCollection("projects/ee-panxinpc/assets/jlborder"),
    geometry = /* color: #98ff00 */ee.Geometry.MultiPoint(),
    table2 = ee.FeatureCollection("projects/ee-panxinpc/assets/jlborder");

var utlload = require('users/panxinpc/paddy:utlload');


//总体参数和尺度
var date1 = "2021-6-01";
var date2 = "2021-7-21";
var mainscale = 20;
//使用可见的蓝绿红
var brandlist = ['B2', 'B3', 'B4'];



var mfc = table;



////将一个Collection中的所有Feature给与序列号,mfc 是列表 mypage是第几块
var serialFunction = function (mfc, mypage) {
    var mylist = mfc.toList(5000000, 0);
    //var mypage=10;
    var newlist = mylist.map(function (element) {
        element = ee.Feature(element);
        var pos = mylist.indexOf(element);
        var temp = ee.Number(mypage).multiply(1000000);
        var lablenumber = temp.add(ee.Number(pos));
        var dict = {
            'LableNumber': lablenumber,
            'PageNumber': mypage,
            'PosNumber': pos
        };
        return element.set(dict);
    });
    return newlist;
}



var first = ee.FeatureCollection([]);
var cumsum = function (currentFeature, featureList) {

    var geometry = currentFeature.geometry();
    var image = utlload.pxLoadS2(geometry, date1, date2, 25);
    var image2 = image;//image.reproject('EPSG:4326', null, mainscale);
    image2 = image2.select(brandlist);
    var cluster = utlload.pxImageClusterOnS2SNIC(image2);
    var cluster2 = cluster.reproject('EPSG:4326', null, mainscale);
    cluster2 = cluster2.select('clusters');
    //产生的Vectors是FeatureCollection格式的
    var vectors = cluster2.reduceToVectors({
        geometryType: 'polygon',
        eightConnected: true,
        scale: mainscale,
        geometry: geometry,
    });
    var pagenumber = ee.Number(currentFeature.get('PageNumber'));
    var mysedvector = serialFunction(vectors, pagenumber)


    featureList = ee.FeatureCollection(featureList);

    return featureList.merge(mysedvector);
};

var result = ee.FeatureCollection(mfc.iterate(cumsum, first));

Export.table.toDrive(
    {
        collection: result,
        description: 'jlobjects',
        folder: 'jldata1',
        fileFormat: 'SHP'
    }
);


