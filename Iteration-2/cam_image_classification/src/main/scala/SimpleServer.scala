/**
  * Created by sudhakar on 2/23/17 and adopted by Raj for Project Sore Vision on 3/5/2017
  * This code creates a simple HTTP server that receives an image and passes it on
  * to Spark for classification as a Cold Sore or a Canker Sore
  */
import java.io.{File, ByteArrayInputStream}
import java.net.InetSocketAddress
import javax.imageio.ImageIO

import com.sun.net.httpserver.{HttpExchange, HttpHandler, HttpServer}
import sun.misc.BASE64Decoder

object SimpleHttpServer extends App{
  val server = HttpServer.create(new InetSocketAddress(8080), 0)
  server.createContext("/get_custom", new RootHandler())
  server.setExecutor(null)
  server.start()
  println("------ waiting for Request ------")
}

class RootHandler extends HttpHandler {
  def handle(httpExchange: HttpExchange) {
    val data = httpExchange.getRequestBody
    val imageByte = (new BASE64Decoder()).decodeBuffer(data)
    val bytes = new ByteArrayInputStream(imageByte)
    val image = ImageIO.read(bytes)
    ImageIO.write(image, "jpg", new File("image.jpg"))
    println("------ Image receiving complete ------")

    // Modified by Raj on 02-27-2017 to call Spark to classify the image
    val response = IPAppTut5.testImage("image.jpg")

    httpExchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*")
    httpExchange.sendResponseHeaders(200, response.length())
    val outStream = httpExchange.getResponseBody
    outStream.write(response.getBytes)
    outStream.close()
  }
}