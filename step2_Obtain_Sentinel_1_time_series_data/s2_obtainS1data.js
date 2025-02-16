var table = ee.FeatureCollection("projects/ee-panxinpc/assets/jlobjectsallpt1");
var utlload = require('users/panxinpc/paddy:utlload');

var dataspan1=['2018-04-10', '2018-04-22', '2018-05-04', '2018-05-16', '2018-05-28', '2018-06-09', '2018-06-21', '2018-07-03', '2018-07-15', '2018-07-27', '2018-08-08', '2018-08-20', '2019-04-10', '2019-04-22', '2019-05-04', '2019-05-16', '2019-05-28', '2019-06-09', '2019-06-21', '2019-07-03', '2019-07-15', '2019-07-27', '2019-08-08', '2019-08-20', '2020-04-10', '2020-04-22', '2020-05-04', '2020-05-16', '2020-05-28', '2020-06-09', '2020-06-21', '2020-07-03', '2020-07-15', '2020-07-27', '2020-08-08', '2020-08-20', '2021-04-10', '2021-04-22', '2021-05-04', '2021-05-16', '2021-05-28', '2021-06-09', '2021-06-21', '2021-07-03', '2021-07-15', '2021-07-27', '2021-08-08', '2021-08-20', ];
var dataspan2=['2018-04-22', '2018-05-04', '2018-05-16', '2018-05-28', '2018-06-09', '2018-06-21', '2018-07-03', '2018-07-15', '2018-07-27', '2018-08-08', '2018-08-20', '2018-09-01', '2019-04-22', '2019-05-04', '2019-05-16', '2019-05-28', '2019-06-09', '2019-06-21', '2019-07-03', '2019-07-15', '2019-07-27', '2019-08-08', '2019-08-20', '2019-09-01', '2020-04-22', '2020-05-04', '2020-05-16', '2020-05-28', '2020-06-09', '2020-06-21', '2020-07-03', '2020-07-15', '2020-07-27', '2020-08-08', '2020-08-20', '2020-09-01', '2021-04-22', '2021-05-04', '2021-05-16', '2021-05-28', '2021-06-09', '2021-06-21', '2021-07-03', '2021-07-15', '2021-07-27', '2021-08-08', '2021-08-20', '2021-09-01', ];
var fieldname=['Y2018N00', 'Y2018N01', 'Y2018N02', 'Y2018N03', 'Y2018N04', 'Y2018N05', 'Y2018N06', 'Y2018N07', 'Y2018N08', 'Y2018N09', 'Y2018N10', 'Y2018N11', 'Y2019N00', 'Y2019N01', 'Y2019N02', 'Y2019N03', 'Y2019N04', 'Y2019N05', 'Y2019N06', 'Y2019N07', 'Y2019N08', 'Y2019N09', 'Y2019N10', 'Y2019N11', 'Y2020N00', 'Y2020N01', 'Y2020N02', 'Y2020N03', 'Y2020N04', 'Y2020N05', 'Y2020N06', 'Y2020N07', 'Y2020N08', 'Y2020N09', 'Y2020N10', 'Y2020N11', 'Y2021N00', 'Y2021N01', 'Y2021N02', 'Y2021N03', 'Y2021N04', 'Y2021N05', 'Y2021N06', 'Y2021N07', 'Y2021N08', 'Y2021N09', 'Y2021N10', 'Y2021N11', ];
var indexname=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, ];

//var featuregroupname=[1,2,3,4,5];//6,7,8,9,10];//,11,12,13,14,15,16,17,18,19,20];//,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,];
var featuregroupname=[10]//,6,7,8,9,10];

var thescale=20;


var dataspanlist1=ee.List(dataspan1);
var dataspanlist2=ee.List(dataspan2);
var reallist=ee.List(indexname);
var fieldnamelist=ee.List(fieldname);

var featuregroupnamelist=ee.List(featuregroupname);

//run a index, for indexname
var runlist=function(current,previousinput){
    var theinput=ee.FeatureCollection(previousinput);
    
    var indexpos=current;
    var date1=dataspanlist1.get(indexpos);
    var date2=dataspanlist2.get(indexpos);
    var targetname=fieldnamelist.get(indexpos);
    
    var geometry=theinput;
    var images1=utlload.pxLoadS1(geometry,date1,date2,'VH');
    
    //var flags=ee.Algorithms.IsEqual(images1)
    
    var flag=ee.Algorithms.IsEqual(images1.bandNames().size(),0);
    
    //obtain s1 success
    var flagfalse=function(images1, geometry, thescale, targetname){
          var myvectors=images1.reduceRegions({
             collection: geometry,
             reducer: ee.Reducer.mean(),
             scale: thescale,  // meters
             crs: 'EPSG:4326',
          });
        
          var myvectors2 = myvectors.map(function(feat){
           
              var kk=feat.set(targetname,feat.get('mean'))
              return kk;
         
          })
          return myvectors2;
    }
    
    //obtain s1 false
    var flagtrue=function(images1, geometry, thescale, targetname){
          var myvectors2 = geometry.map(function(feat){
              var kk=feat.set(targetname,-50)
              return kk;
          })
          return myvectors2;
    }
    
    var returnvalue = ee.Algorithms.If(flag, flagtrue(images1, geometry, thescale, targetname), flagfalse(images1, geometry, thescale, targetname));
    return returnvalue;
}

//run a list2 in featuregroupname
var runfeaturegroup=function(current,previousinput){
    var cf=current;
    var pcf=ee.FeatureCollection(previousinput);
   
    var subgeom=table.filter(ee.Filter.equals('PageNumber', cf));//.filter(ee.Filter.lessThan('PosNumber', 10));
    
    //subgeom=ee.FeatureCollection(subgeom.toList(2)); in my test, try to use less data;
    
    var first=subgeom;
    var result=ee.FeatureCollection(reallist.iterate(runlist,first));
    var result2=result.map(function(feat){
      return feat.setGeometry(null);
    });
    
    return pcf.merge(result2);
   
}


var featfirst = ee.FeatureCollection([]);
var thelastresult=ee.FeatureCollection(featuregroupnamelist.iterate(runfeaturegroup,featfirst));

Export.table.toDrive(
  {
     collection: thelastresult,
     description:'s1collectpt102E',
     folder: 's1collectpt1',
     fileFormat: 'CSV'
  }
);



