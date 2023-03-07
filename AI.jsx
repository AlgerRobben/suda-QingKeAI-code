sourceFolder = new Folder("C:/Users/lenovo/Desktop/¿òÏßÍ¼");
destFolder = new Folder("C:/Users/lenovo/Desktop/aiÍ¼");



// Collectable files
var COLLECTABLE_EXTENSIONS = ["bmp", "gif", "giff", "jpeg", "jpg", "pct", "pic", "psd", "png", "tif", "tiff"];
   
var destFolder, sourceFolder;


if(sourceFolder != null && destFolder != null)
{
        //getting the list of the files from the input folder
        var fileList = sourceFolder.getFiles();
        var errorList;
        var tracingPresets = app.tracingPresetsList;

        for (var i=0; i<fileList.length; ++i)
        {
            if (fileList[i] instanceof File)
            {
                 try
                 {                
                        var fileExt = String(fileList[i]).split (".").pop();
                        if(isTraceable(fileExt) != true)
                            continue;
                        
                        // Trace the files by placing them in the document.

                        // Add a document in the app
                        var doc = app.documents.add();
                        
                        // Add a placed item
                        var p = doc.placedItems.add();
                        p.file = new File(fileList[i]);
                        
                        // Trace the placed item
                        var t = p.trace();
                        t.tracing.tracingOptions.loadFromPreset(tracingPresets[4]);
                        app.redraw();
 
                        var destFileName = fileList[i].name.substring(0, fileList[i].name.length - fileExt.length-1) + "_" +fileExt;
                        var outfile = new File(destFolder+"/"+destFileName);
                        doc.saveAs(outfile);
                        doc.close();
                }
                catch (err)
                {
                        errorStr = ("Error while tracing "+ fileList[i].name  +".\n" + (err.number & 0xFFFF) + ", " + err.description);
                        // alert(errorStr);
                        errorList += fileList[i].name + " ";
                }
            }
       }
       fileList = null;
       alert("Batch process complete.");
}
else
{
       alert("Batch process aborted.");
}

 sourceFolder = null;
 destFolder = null;
 
function isTraceable(ext)
 {
     var result = false;
     for (var i=0; i<COLLECTABLE_EXTENSIONS.length; ++i)
     {
          if(ext == COLLECTABLE_EXTENSIONS[i])
          {
            result = true;
            break;
          }
    }
    return result;
}	