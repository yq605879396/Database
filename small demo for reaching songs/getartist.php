<html>
 <head>
  <title> Kumi</title>
 </head>
 <body>
    <?php echo "<br/>Here is the information of artist from ".$_POST["nation"].":<br/><br/>"; ?>

    <?php  
    $link = mysqli_connect('localhost:3306', 'root', '*****', '***'); // filled in your own password and databasename   
     
     if (!$link) 
     {  
         printf("Woops.. Something wrong when connecting to MySQL Server. Errorcode: %s ", mysqli_connect_error()); 
         exit; 
     }
     else
     { 
         //echo ('Succeed Connected')."<br/>";   /* Close the connection 关闭连接*/
     }
      
     mysqli_query($link,'set names utf8');    //解决中文乱码的问题
     $query =  "SELECT distinct(artistId),artistName, albumName, ltime
                FROM (SELECT artistId, min(releaseTime) as ltime
                    FROM song natural join songinalbum 
                    where artistId in (select artistId from artist where nationality = '".$_POST["nation"]."')
                    group by artistId) as latesttime natural join (select sid,artistId from song) as s natural join songinalbum natural join album natural join artist
                where releaseTime = ltime;";

     //echo $query, "<br/>";  

     if ($result = mysqli_query($link, $query))  
     {
        echo "<div style='white-space:pre'>";   
        echo sprintf("\t \t \t %-15s \t %-35s \t %-15s\n", "Artist Name", "Ablum Name", "Release Time"); 
        echo "<br>";
        //echo "</div>";

        //$output = sprintf("Australia comprises %d states and %d territories <\pre>", str_pad(2,10," ",STR_PAD_LEFT),10);
        //echo "<pre white-space:pre>", $output, "</pre>";
        while( $row = mysqli_fetch_assoc($result) )
        {  
            //echo "<div class='layout' style='white-space:pre'>"; 
            echo "<input type='button' name='check' value='details' onclick=display('show".$row["artistId"]."')>";
            echo sprintf("\t \t %-15s \t %-35s \t %-15s ", $row["artistName"], $row["albumName"],  $row["ltime"]);
            //echo "<br>";  
            //echo sprintf("\t \t %-25s %-45s %-15s \n", $row["artistName"], $row["albumName"],  $row["ltime"]);             
            $query_with_id = "SELECT distinct(sname), language, style, duration, releasetime
                            from song
                            where artistId = '".$row["artistId"]."'
                            order by releasetime desc, sname asc";
            if ($data = mysqli_query($link, $query_with_id))
            {   

                echo "<div id='show".$row["artistId"]."' style='display:none'>";  
                //echo '<pre>'.print_r($data,1).'</pre>'; 
                $output = sprintf("\n\t \t %-25s \t \t \t %-15s \t %-15s \t %-25s \t %-25s \n\n", "song name", "language", "style", "duration", "releasetime");
                echo $output;
                while( $tuple = mysqli_fetch_assoc($data) )
                {
                    echo sprintf("\t \t %-25s \t \t \t %-15s \t %-15s \t %-25s \t %-25s \n", $tuple["sname"], $tuple["language"], $tuple["style"], $tuple["duration"], $tuple["releasetime"]);
                    //echo sprintf("\t \t %-45s  %-35s  %-35s  %-15s  %-25s \n", $tuple["sname"], $tuple["language"], $tuple["style"], $tuple["duration"], $tuple["releasetime"]);
                }
                echo "</div>";
                echo "\n\n";
            }
        }   
        /* Destroy the result set and free the memory used for it 结束查询释放内存 */
        echo "</div>";
        mysqli_free_result($result); 
     
     }  
     
     /* Close the connection 关闭连接*/ 
     mysqli_close($link);
     
     ?> 

    <?php   echo "<script language=javascript>
                  function display(artistid){
                        var t = document.getElementById(artistid);
                        if(t.style.display == 'none') {
                            t.style.display = 'block';
                        } else {
                            t.style.display = 'none';            
                     }
                    }

                    </script>"; ?>

 </body>
</html>