
<?php include("header.php"); ?>

    <!-- Navbar & Hero End -->
<br><br><br>

   


    <!-- Destination Start -->
    <div class="container-xxl py-5 destination">
        <div class="container">
            <div class="text-center wow fadeInUp" data-wow-delay="0.1s">
                <!-- <h6 class="section-title bg-white text-center text-primary px-3">Plan Your Trip With Us</h6> -->
                <h1 class="mb-5">Vandalism Detection </h1>
            </div>
            <div class="row g-3">
                <div class="col-lg-12 col-md-12">

                <?php 
                 set_time_limit(0);

                $python =`python  test.py`;
                 
                ?>

                   
                CAM  OPENED Detection Started ...
                </div>
            </div>
        </div>
    </div>
    <!-- Destination Start -->
<br>
<br>
<br>
<br>
<br>
<br>


        
    <?php include("footer.php"); ?>
