using System;
using Slidessibility.Core; // This works because of your reference link!

namespace Slidessibility.CLI
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Starting Slidessibility CLI Tool...");
            
            // Call the engine method
            string message = AccessibilityEngine.TestConnection();
            Console.WriteLine(message);
        }
    }
}