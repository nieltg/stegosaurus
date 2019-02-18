using Gee;

namespace Stegosaurus {

  public struct Header {
    public string name;
    public bool one_bit;
    public bool is_frame_acak;
    public bool is_pixel_acak;
  }

  public class RandomCursor : GLib.Object {
    private Iterator<int> valuesIterator;

    public RandomCursor(int seed, int start, int end) {
      GLib.Random.set_seed(seed);
      var values = new ArrayList<int> ();
      while (values.size < end-start) {
        int number = GLib.Random.int_range(start, end);
        if (values.contains(number)){
            continue;
        }
        values.add(number);
      }
      this.valuesIterator = values.iterator();
    }
    public bool next(out int result) {
      if (this.valuesIterator.next()){
          result = this.valuesIterator.get();
          return true;
      }
      return false;
    } 
  }
  public class Random : GLib.Object {
    public Random() {
      
    }
    public RandomCursor rand_int(int seed, int start, int end){
      return new RandomCursor(seed, start, end);
    }
  }

  public class Encoder : GLib.Object {
    protected static string stego = "STEGOSAURUS";
    public Encoder(){

    }
    public uint8[] encode_header(Header header){
      var result = new uint8[Encoder.stego.char_count()+1+header.name.char_count()+1];
      for (int i=0; i<Encoder.stego.char_count(); i++){
        result[i] = (uint8)Encoder.stego[i];
      }
      uint8 flag = 0 | (header.one_bit?1<<2:0) | (header.is_frame_acak?1<<1:0) | (header.is_pixel_acak?1:0);
      result[Encoder.stego.char_count()] = flag;
      for (int i=0; i<header.name.char_count(); i++){
        result[Encoder.stego.char_count()+1+i] = header.name[i];
      }
      result[result.length-1] = 0;
      return result;
    }
  }

  public class Decoder : GLib.Object {
    protected static string stego = "STEGOSAURUS";
    public bool is_stego = true;
    private Header header;

    public Decoder(){
      this.header = Header(){
        name = "",
        one_bit = false,
        is_frame_acak = false,
        is_pixel_acak = false
      };
    }
    public bool decode_header(int i, uint8 byte_stream){
      if(byte_stream == 0 || !this.is_stego){
        return false;
      }
      if(i<Decoder.stego.char_count()){
        // inspect stego flag
        this.is_stego = this.inspect_stego(i, byte_stream);
      } else if(i==Decoder.stego.char_count()){
        // get flag properties
        this.header.one_bit = (byte_stream & 1<<2) > 0;
        this.header.is_frame_acak = (byte_stream & 1<<1) > 0;
        this.header.is_pixel_acak = (byte_stream & 1) > 0;
      } else {
        // get filename
        this.header.name += ((char)byte_stream).to_string();
      }
      return true;
    }
    public Header get_header(){
      return this.header;
    }
    public bool inspect_stego(int i, uint8 byte_stream){
      if (byte_stream == (uint8) this.stego[i]){
        return true;
      }
      return false;
    }
  }

  static int main (string[] args){
    // Example random
    Random rand = new Random();
    RandomCursor randCursor = rand.rand_int(0, 0, 10);
    int res;
    while (randCursor.next(out res)){
      stdout.printf("%d\n", res);
    }

    // Example encode
    var encoder = new Encoder();
    var result = encoder.encode_header(Header(){
      name = "santi.txt",
      one_bit = false,
      is_frame_acak = true,
      is_pixel_acak = true
    });

    // Example decode
    var decoder = new Decoder();
    int i=0;
    while (decoder.decode_header(i, result[i])){
      i++;
    }
    if (decoder.is_stego){
      var header = decoder.get_header();
      stdout.printf("%s\n", header.name);
      stdout.printf("%d\n", (int) header.one_bit);
      stdout.printf("%d\n", (int) header.is_frame_acak);
      stdout.printf("%d\n", (int) header.is_pixel_acak);
    }

    // Example decode 2
    char[] bytes = new char[4]{'S', 'T', 'g', 's'};

    decoder = new Decoder();
    i=0;
    while (decoder.decode_header(i, bytes[i])){
      i++;
    }
    if (decoder.is_stego){
      var header = decoder.get_header();
      stdout.printf("%s\n", header.name);
      stdout.printf("%d\n", (int) header.one_bit);
      stdout.printf("%d\n", (int) header.is_frame_acak);
      stdout.printf("%d\n", (int) header.is_pixel_acak);
    }
    return 0;
  }
}