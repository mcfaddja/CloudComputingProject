package com.amazonaws.samples;

import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;

public class DataGenerator {
	
	public static void main(String args[]) throws IOException
	{
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(
          new FileOutputStream("data.txt"), "utf-8"));
		
		System.out.println("Started writting");
		
		for(int i = 0; i < 30000000; i++)
		{
			Item data_item = new Item(Integer.toString(i), "demo" + Integer.toString(i));
			bw.write(data_item.getId() + "," + data_item.getName());
			bw.newLine();
		}
		
		System.out.println("Stopped writting");
		
		bw.flush();
		bw.close();
	}
}
